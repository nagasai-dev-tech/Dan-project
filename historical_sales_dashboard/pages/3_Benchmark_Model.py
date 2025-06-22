import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils.loader import load_branch_data

st.set_page_config(layout="wide")
st.title("🎯 WA Benchmark-Based Target Model for NSW & QLD")

# Load and preprocess
wa, nsw, qld = load_branch_data()
for df in [wa, nsw, qld]:
    df["Issue Date"] = pd.to_datetime(df["Issue Date"], dayfirst=True, errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    df.dropna(subset=["Issue Date", "Total"], inplace=True)

# Weekly aggregation
wa_weekly = wa.groupby(pd.Grouper(key="Issue Date", freq="W"))["Total"].sum().reset_index(name="WA Sales")
nsw_weekly = nsw.groupby(pd.Grouper(key="Issue Date", freq="W"))["Total"].sum().reset_index(name="NSW Sales")
qld_weekly = qld.groupby(pd.Grouper(key="Issue Date", freq="W"))["Total"].sum().reset_index(name="QLD Sales")

min_len = min(len(wa_weekly), len(nsw_weekly), len(qld_weekly))
wa_weekly, nsw_weekly, qld_weekly = wa_weekly.iloc[:min_len], nsw_weekly.iloc[:min_len], qld_weekly.iloc[:min_len]

# WA growth rate
wa_weekly["Growth"] = wa_weekly["WA Sales"].pct_change()
wa_growth = wa_weekly["Growth"].mean()

# Build targets for NSW and QLD
def build_target_model(actual_df, sales_col, growth, label):
    df = actual_df.copy()
    initial = df[sales_col].iloc[0]
    df["Target Sales"] = [initial * (1 + growth) ** i for i in range(len(df))]
    df["Difference"] = df[sales_col] - df["Target Sales"]
    df["Deviation %"] = (df["Difference"] / df["Target Sales"]) * 100
    df["Branch"] = label
    return df

nsw_model = build_target_model(nsw_weekly, "NSW Sales", wa_growth, "NSW")
qld_model = build_target_model(qld_weekly, "QLD Sales", wa_growth, "QLD")

# Combine
all_data = pd.concat([nsw_model[["Issue Date", "Branch", "NSW Sales", "Target Sales", "Difference", "Deviation %"]],
                      qld_model[["Issue Date", "Branch", "QLD Sales", "Target Sales", "Difference", "Deviation %"]]])

# Rename actual sales column to unify
all_data["Actual Sales"] = all_data["NSW Sales"].combine_first(all_data["QLD Sales"])
all_data.drop(columns=["NSW Sales", "QLD Sales"], inplace=True)

# ---------------------- COMPARISON CHART ----------------------
st.subheader("📈 Weekly Sales vs WA-Based Target")
fig, ax = plt.subplots(figsize=(14, 5))
for branch in all_data["Branch"].unique():
    branch_df = all_data[all_data["Branch"] == branch]
    sns.lineplot(data=branch_df, x="Issue Date", y="Actual Sales", label=f"{branch} Sales", linewidth=2)
    sns.lineplot(data=branch_df, x="Issue Date", y="Target Sales", label=f"{branch} Target", linestyle="--")
ax.set_title("Branch Sales vs WA-Based Target")
ax.set_ylabel("Sales ($)")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# ---------------------- KPI SCORECARD ----------------------
st.subheader("📊 KPI Scorecard")
scorecards = []
for branch in all_data["Branch"].unique():
    latest = all_data[all_data["Branch"] == branch].dropna().iloc[-1]
    scorecards.append({
        "Branch": branch,
        "Actual": latest["Actual Sales"],
        "Target": latest["Target Sales"],
        "Delta": latest["Actual Sales"] - latest["Target Sales"],
        "Deviation %": latest["Deviation %"]
    })

kpi_df = pd.DataFrame(scorecards)
kpi_cols = st.columns(len(kpi_df))
for i, row in kpi_df.iterrows():
    kpi_cols[i].metric(
        f"{row['Branch']} Achievement",
        f"${row['Actual']:,.0f}",
        delta=f"{row['Deviation %']:.1f}%",
        delta_color="inverse" if row["Deviation %"] < 0 else "normal"
    )

# ---------------------- DEVIATION TABLE ----------------------
st.subheader("📋 Weekly Deviation Table")

def deviation_color(val):
    if abs(val) > 10:
        return "background-color: #ffdddd"
    elif abs(val) > 5:
        return "background-color: #fff2cc"
    else:
        return "background-color: #e6ffe6"

df_to_display = all_data[["Issue Date", "Branch", "Actual Sales", "Target Sales", "Difference", "Deviation %"]].copy()
df_to_display = df_to_display.reset_index(drop=True)

st.dataframe(
    df_to_display.style
        .format({
            "Actual Sales": "${:,.0f}",
            "Target Sales": "${:,.0f}",
            "Difference": "${:,.0f}",
            "Deviation %": "{:+.1f}%"
        })
        .applymap(deviation_color, subset=["Deviation %"])
)

# ---------------------- QUARTERLY COMPARISON ----------------------
st.subheader("📆 Quarterly Sales Comparison")
all_data["Quarter"] = all_data["Issue Date"].dt.to_period("Q")
quarterly_summary = all_data.groupby(["Quarter", "Branch"])[["Actual Sales", "Target Sales"]].sum().reset_index()
quarter_pivot = quarterly_summary.pivot(index="Quarter", columns="Branch", values="Actual Sales")
st.bar_chart(quarter_pivot)

# ---------------------- DOWNLOAD ----------------------
st.subheader("📥 Download Full Weekly Comparison")
export_df = all_data[["Issue Date", "Branch", "Actual Sales", "Target Sales", "Difference", "Deviation %"]]
csv_data = export_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv_data, "branch_vs_target.csv", "text/csv")
