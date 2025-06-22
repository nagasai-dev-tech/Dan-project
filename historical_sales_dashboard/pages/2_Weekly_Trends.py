import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from prophet import Prophet
from sklearn.linear_model import LinearRegression
import numpy as np
from utils.loader import load_branch_data

st.set_page_config(layout="wide")
st.title("📊 Weekly Sales Analysis & Forecast Dashboard")

wa, nsw, qld = load_branch_data()
branch = st.selectbox("🏢 Select Branch", ["WA", "NSW", "QLD"])
data = {"WA": wa, "NSW": nsw, "QLD": qld}[branch]

if "Issue Date" in data.columns and "Total" in data.columns:
    # 🧼 Clean and prep data
    data["Issue Date"] = pd.to_datetime(data["Issue Date"], dayfirst=True, errors="coerce")
    data["Total"] = pd.to_numeric(data["Total"], errors="coerce")
    data = data.dropna(subset=["Issue Date", "Total"])
    data = data.sort_values("Issue Date")

    # Time fields
    data["Week"] = data["Issue Date"].dt.to_period("W").apply(lambda r: r.start_time)
    data["Quarter"] = data["Issue Date"].dt.to_period("Q")
    data["Year"] = data["Issue Date"].dt.year

    # Weekly Aggregation
    weekly = data.groupby("Week")["Total"].sum().reset_index()
    weekly.columns = ["ds", "y"]

    # 📈 Weekly Sales with Rolling Average
    st.subheader(f"📈 Weekly Sales with Rolling Average - {branch}")
    window = st.slider("Select rolling window (weeks)", 2, 12, 4)
    weekly["Rolling Avg"] = weekly["y"].rolling(window=window).mean()

    fig1, ax1 = plt.subplots(figsize=(12, 4))
    sns.lineplot(data=weekly, x="ds", y="y", label="Weekly Sales", marker="o", color="#007ACC", ax=ax1)
    sns.lineplot(data=weekly, x="ds", y="Rolling Avg", label=f"{window}-Week Avg", color="orange", ax=ax1)
    ax1.set_title(f"{branch} - Weekly Sales & {window}-Week Avg")
    ax1.set_ylabel("Total Sales")
    ax1.grid(True)
    st.pyplot(fig1)

    # 📏 Linear Trend Line
    st.subheader("📏 Sales Trend - Linear Regression")
    weekly["ds_ordinal"] = pd.to_datetime(weekly["ds"]).map(pd.Timestamp.toordinal)
    x = weekly["ds_ordinal"].values.reshape(-1, 1)
    y = weekly["y"].values
    reg = LinearRegression().fit(x, y)
    weekly["Trend"] = reg.predict(x)

    fig2, ax2 = plt.subplots(figsize=(12, 4))
    sns.lineplot(x=weekly["ds"], y=weekly["y"], label="Actual", marker="o", ax=ax2)
    sns.lineplot(x=weekly["ds"], y=weekly["Trend"], label="Linear Fit", color="green", ax=ax2)
    ax2.set_title("Trend Slope - Fitted Line")
    ax2.grid(True)
    st.pyplot(fig2)

    # 🔮 Prophet Forecast
    st.subheader("🔮 Prophet Forecast (Next 12 Weeks)")
    model = Prophet()
    model.fit(weekly[["ds", "y"]])

    future = model.make_future_dataframe(periods=12, freq="W")
    forecast = model.predict(future)

    fig3 = model.plot(forecast)
    st.pyplot(fig3)

    st.dataframe(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12).rename(columns={
            "ds": "Date",
            "yhat": "Forecast",
            "yhat_lower": "Low Estimate",
            "yhat_upper": "High Estimate"
        }).style.format({"Forecast": "{:,.0f}", "Low Estimate": "{:,.0f}", "High Estimate": "{:,.0f}"}))

    # ⚠️ Quarter over Quarter % Drop
    st.subheader("⚠️ Customer Drop >30%: Quarter-over-Quarter")

    qtr_customer_sales = data.groupby(["Top Level Customer Name", "Quarter"])["Total"].sum().reset_index()
    pivot_qtr = qtr_customer_sales.pivot(index="Top Level Customer Name", columns="Quarter", values="Total")
    pivot_qtr = pivot_qtr.apply(pd.to_numeric, errors='coerce')
    pct_change_qtr = pivot_qtr.pct_change(axis=1) * 100

    if pct_change_qtr.shape[1] >= 2:
        latest_qtr = pct_change_qtr.columns[-1]
        drop_alerts = pct_change_qtr[pct_change_qtr[latest_qtr] < -30][[latest_qtr]].dropna().round(1)
        drop_alerts.columns = ["% Drop from Last Quarter"]
        drop_alerts = drop_alerts.sort_values(by="% Drop from Last Quarter")

        st.dataframe(drop_alerts.style.background_gradient(cmap="Reds").format("{:+.1f}%"))

        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=True, sheet_name="Alerts")
            return output.getvalue()

        st.download_button(
            label="📥 Download Alerts Report",
            data=to_excel(drop_alerts),
            file_name=f"{branch}_Customer_Drops.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Not enough quarters to calculate drop alerts.")

    # 👑 Top Customers - Rolling View
    st.subheader("👑 Top Customers in Rolling Weeks")
    num_weeks = st.slider("Rolling Weeks", 4, 26, 13)
    recent_weeks = sorted(data["Week"].unique())[-num_weeks:]
    rolling_data = data[data["Week"].isin(recent_weeks)]
    top_customers = (
        rolling_data.groupby("Top Level Customer Name")["Total"]
        .sum().sort_values(ascending=False).head(10).reset_index()
    )
    st.dataframe(top_customers.rename(columns={"Total": f"Total Last {num_weeks} Weeks"}).style.format({f"Total Last {num_weeks} Weeks": "{:,.0f}"}))

else:
    st.error("❌ Missing required columns: 'Issue Date' and 'Total'")
