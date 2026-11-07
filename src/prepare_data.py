from pathlib import Path

import pandas as pd

RAW_FOLDER = Path("data/raw")
OUTPUT_FILE = Path("data/processed/monthly.csv")

def load_cpi():
    cpi = pd.read_csv(RAW_FOLDER / "cpi_rate.csv", header=None, names=["period", "cpi_rate"])
    cpi = cpi[cpi["period"].str.match(r"^\d{4} [A-Z]{3}$")].copy()
    cpi["date"] = pd.to_datetime(cpi["period"], format="%Y %b")
    cpi["cpi_rate"] = pd.to_numeric(cpi["cpi_rate"])
    return cpi.set_index("date")[["cpi_rate"]].sort_index()

def load_fred(file_name, new_name):
    table = pd.read_csv(RAW_FOLDER / file_name, parse_dates=["observation_date"])
    table = table.set_index("observation_date")
    table.columns = [new_name]
    return table

def build_table():
    cpi = load_cpi()
    oil = load_fred("brent_oil.csv", "oil_usd")
    pound = load_fred("usd_per_gbp.csv", "usd_per_gbp")
    table = cpi.join(oil, how="left").join(pound, how="left")
    table.index.name = "date"
    return table

if __name__ == "__main__":
    table = build_table()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT_FILE)
    print(table.tail())
    print(f"\n{len(table)} months, from {table.index[0]:%b %Y} to {table.index[-1]:%b %Y}")
    print("\nMissing values in each column:")
    print(table.isna().sum())