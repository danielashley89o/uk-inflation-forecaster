import pandas as pd

from backtest import backtest, load_data
from models import ridge_forecast

data = load_data()
next_month = data.index[-1] + pd.DateOffset(months=1)
forecast = ridge_forecast(data)

# How far out was the model in the past? Use the middle 80% of its errors.
past_errors = backtest(ridge_forecast, data)["error"]
low = forecast - past_errors.quantile(0.9)
high = forecast - past_errors.quantile(0.1)

print(f"Latest inflation ({data.index[-1]:%B %Y}): {data['cpi_rate'].iloc[-1]}%")
print(f"Forecast for {next_month:%B %Y}: {forecast:.1f}%")
print(f"Likely range (about 8 times in 10): {low:.1f}% to {high:.1f}%")