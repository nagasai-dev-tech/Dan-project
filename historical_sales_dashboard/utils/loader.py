import pandas as pd
import os

# Base data directory (relative path)
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# 1. For Lifecycle Comparison
def load_historical_report():
    path = os.path.join(DATA_DIR, "HISTORICAL_REPORT.xlsx")
    return pd.ExcelFile(path)

# 2. For Weekly Trends, Benchmark, and Customer Analysis
def load_branch_data():
    wa_path = os.path.join(DATA_DIR, "WA.CSV")
    nsw_path = os.path.join(DATA_DIR, "NSW.CSV")
    qld_path = os.path.join(DATA_DIR, "QLD.CSV")

    wa_df = pd.read_csv(wa_path)
    nsw_df = pd.read_csv(nsw_path)
    qld_df = pd.read_csv(qld_path)

    return wa_df, nsw_df, qld_df
