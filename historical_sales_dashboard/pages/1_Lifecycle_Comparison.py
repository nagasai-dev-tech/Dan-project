import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.loader import load_historical_report

st.set_page_config(layout="wide")
st.title("🌱 Branch Lifecycle Comparison (Yearly)")

# ------------------ LOAD ---------------------
try:
    xls = load_historical_report()
    sheet = st.selectbox("📄 Select a Sheet", xls.sheet_names)
    df = pd.read_excel(xls, sheet_name=sheet)
    df.columns = df.columns.str.strip()

    # ------------------ CLEAN ---------------------
    year_cols = [col for col in df.columns if "/" in col]
    branches = df["Financial Year"].dropna().astype(str)

    melted = df.melt(id_vars="Financial Year", value_vars=year_cols,
                     var_name="Year", value_name="Sales")
    melted["Sales"] = pd.to_numeric(melted["Sales"], errors="coerce")

    # ------------------ FILTER ---------------------
    selected_branches = st.multiselect("🏢 Select Branches to Compare", branches.unique(), default=branches.unique())
    filtered_df = melted[melted["Financial Year"].isin(selected_branches)]

    # ------------------ PIVOT FOR VISUALS ---------------------
    pivot_table = filtered_df.pivot_table(index="Year", columns="Financial Year", values="Sales", aggfunc='sum')

    # ------------------ PLOT 1: Line Chart ---------------------
    st.subheader("📈 YOY Sales Trends by Branch")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=filtered_df, x="Year", y="Sales", hue="Financial Year", marker="o", palette="Set2", ax=ax1)
    ax1.set_title("Sales Trend Over Years", fontsize=14)
    ax1.set_ylabel("Sales")
    ax1.set_xlabel("Year")
    ax1.grid(True)
    st.pyplot(fig1)

    # ------------------ PLOT 2: Bar Chart ---------------------
    st.subheader("📊 Total Sales per Year per Branch")
    st.bar_chart(pivot_table)

    # ------------------ PLOT 3: Heatmap ---------------------
    st.subheader("🔥 Sales Heatmap")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot_table.T, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=0.5, ax=ax2)
    ax2.set_title("Branch Sales by Year (Heatmap)", fontsize=14)
    st.pyplot(fig2)

    # ------------------ TABLE 1: YOY % Change ---------------------
    st.subheader("📉 YOY % Change per Branch")
    yoy_change = pivot_table.pct_change().multiply(100).round(1)
    st.dataframe(yoy_change.style.background_gradient(cmap="RdYlGn_r").format("{:+.1f}%"))

    # ------------------ TABLE 2: Total Sales Ranking ---------------------
    st.subheader("🏆 Branch Ranking by Total Sales")
    rank_df = pivot_table.sum().sort_values(ascending=False).reset_index()
    rank_df.columns = ["Branch", "Total Sales"]
    rank_df["Rank"] = rank_df["Total Sales"].rank(ascending=False).astype(int)
    st.dataframe(rank_df.style.highlight_max(axis=0, color="lightgreen").format({"Total Sales": "{:,.0f}"}))

    # ------------------ DOWNLOAD BUTTON ---------------------
    st.download_button(
        label="📥 Download YOY % Change Data",
        data=yoy_change.to_csv().encode('utf-8'),
        file_name='yoy_percent_change.csv',
        mime='text/csv'
    )

except FileNotFoundError:
    st.error("🚫 'HISTORICAL_REPORT.xlsx' not found in the /data folder. Please upload it to proceed.")
