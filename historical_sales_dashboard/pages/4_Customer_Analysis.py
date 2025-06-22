import streamlit as st
import pandas as pd
import seaborn as sns
from utils.loader import load_branch_data

st.set_page_config(layout="wide")
st.title("🧍 Customer Spend Breakdown, Trends & Drop Alerts")

# -------------------- Load and Merge --------------------
wa, nsw, qld = load_branch_data()
wa["Branch"] = "WA"
nsw["Branch"] = "NSW"
qld["Branch"] = "QLD"
df = pd.concat([wa, nsw, qld], ignore_index=True)

# -------------------- Validation --------------------
required_cols = ["Issue Date", "Total", "Top Level Customer Name", "Branch"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    st.error(f"Missing columns: {', '.join(missing)}")
    st.stop()

# -------------------- Preprocess --------------------
df["Issue Date"] = pd.to_datetime(df["Issue Date"], errors='coerce')
df = df.dropna(subset=["Issue Date", "Total", "Top Level Customer Name", "Branch"])
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df["Quarter"] = df["Issue Date"].dt.to_period("Q")
df["Week"] = df["Issue Date"].dt.to_period("W")

# -------------------- Filters --------------------
branches = df["Branch"].unique().tolist()
selected_branches = st.multiselect("🏢 Select Branches", branches, default=branches)
filtered_df = df[df["Branch"].isin(selected_branches)]

customers = filtered_df["Top Level Customer Name"].unique().tolist()
selected_customer = st.selectbox("👤 Select Customer", sorted(customers))
customer_df = filtered_df[filtered_df["Top Level Customer Name"] == selected_customer]

# -------------------- Weekly Spend Trend --------------------
st.subheader(f"📅 Weekly Spend Trend: {selected_customer}")
weekly = customer_df.groupby("Week")["Total"].sum().reset_index()
if not weekly.empty:
    st.line_chart(weekly.set_index("Week")["Total"])
else:
    st.info("No weekly data available.")

# -------------------- Quarterly Spend Table --------------------
st.subheader("📆 Quarterly Spend Summary")
quarterly = filtered_df.groupby(["Top Level Customer Name", "Branch", "Quarter"])["Total"].sum().reset_index()
pivot = quarterly.pivot_table(index="Quarter", columns="Top Level Customer Name", values="Total")

# -------------------- Drop Alert Logic --------------------
alerts = []
for customer in pivot.columns:
    for i in range(4, len(pivot)):
        current = pivot.iloc[i][customer]
        last_year = pivot.iloc[i - 4][customer]
        if pd.notna(current) and pd.notna(last_year):
            drop_pct = ((last_year - current) / last_year) * 100
            if drop_pct > 30:
                alerts.append({
                    "Customer": customer,
                    "Quarter": str(pivot.index[i]),
                    "Drop %": round(drop_pct, 1),
                    "Previous Spend": last_year,
                    "Current Spend": current
                })

# -------------------- Show Alerts --------------------
st.subheader("🚨 Customers with >30% Spend Drop YoY")
if alerts:
    alert_df = pd.DataFrame(alerts).sort_values(by="Drop %", ascending=False)
    st.dataframe(alert_df.style.format({
        "Drop %": "{:.1f}%",
        "Previous Spend": "₹{:,.0f}",
        "Current Spend": "₹{:,.0f}"
    }))

    # 🏆 Top 5 Drop Summary
    st.markdown("### 🏆 Top 5 Drop Alerts")
    top5 = alert_df.head(5)
    st.table(top5[["Customer", "Quarter", "Drop %"]].style.highlight_max(axis=0, color="salmon"))
else:
    st.success("✅ No major drop detected over the last four quarters.")

# -------------------- Optional Raw Data Toggle --------------------
with st.expander("📂 Show Raw Data (filtered)"):
    st.dataframe(filtered_df.head(100))

# -------------------- Quarter-over-Quarter Growth Analysis --------------------
st.subheader("📈 Quarter-over-Quarter (QoQ) Growth Rate")

qoq_growth = pivot.pct_change().multiply(100).round(1)

qoq_view = st.radio("View QoQ Growth for", ["All Customers", "Selected Customer Only"])
light_cmap = sns.light_palette("green", as_cmap=True)

if qoq_view == "Selected Customer Only":
    if selected_customer in qoq_growth.columns:
        qoq_selected = qoq_growth[[selected_customer]]
        st.dataframe(qoq_selected.style
                     .format("{:+.1f}%")
                     .background_gradient(cmap=light_cmap))
    else:
        st.warning("Selected customer not available in QoQ data.")
else:
    st.dataframe(qoq_growth.style
                 .format("{:+.1f}%")
                 .background_gradient(cmap="BuGn"))
