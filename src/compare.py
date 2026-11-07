from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from backtest import average_error, backtest, load_data, naive_forecast
from models import arima_forecast, ridge_forecast

METHODS = {"Naive": naive_forecast, "ARIMA": arima_forecast, "Ridge": ridge_forecast}
PERIODS = {
    "Whole test": ("2015-01-01", None),
    "Before the shock (2015-2020)": ("2015-01-01", "2020-12-31"),
    "Inflation shock (2021-2023)": ("2021-01-01", "2023-12-31"),
    "Since then (2024 onwards)": ("2024-01-01", None),
}

data = load_data()
all_results = {name: backtest(method, data) for name, method in METHODS.items()}


table = pd.DataFrame(
    {
        period: {name: average_error(results.loc[start:end]) for name, results in all_results.items()}
        for period, (start, end) in PERIODS.items()
    }
).round(3)
print("Average error, in percentage points (lower is better):\n")
print(table.to_string())

naive_miss = all_results["Naive"]["error"].abs()
ridge_miss = all_results["Ridge"]["error"].abs()
print(f"\nRidge closer than Naive: {(ridge_miss < naive_miss).sum()} months")
print(f"Naive closer than Ridge: {(naive_miss < ridge_miss).sum()} months")
print(f"Exactly tied: {(naive_miss == ridge_miss).sum()} months")

Path("results").mkdir(exist_ok=True)
table.to_csv("results/comparison.csv")

ridge = all_results["Ridge"]
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(ridge.index, ridge["actual"], color="black", linewidth=2, label="Actual")
ax.plot(ridge.index, ridge["forecast"], color="#c0392b", linewidth=1.2, label="Ridge forecast")
ax.set_title("Ridge forecasts one month ahead vs actual UK CPI inflation")
ax.set_ylabel("% change on a year earlier")
ax.legend()
fig.tight_layout()
fig.savefig("charts/forecast_vs_actual.png", dpi=150)
print("\nSaved results/comparison.csv and charts/forecast_vs_actual.png")