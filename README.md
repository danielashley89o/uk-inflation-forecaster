# UK Inflation Forecaster

Can public data beat the simple guess that next month's UK inflation
will equal this month's? Slightly, but not by enough to rule out luck.

![Forecast vs actual](charts/forecast_vs_actual.png)


Ridge was closer in 80 months and the simple guess in 61 (sign test p = 0.13).

## What I learned

- Annual inflation has built-in inertia because consecutive readings share 11 of their 12 months. The correlation with the previous month is 0.985, and 53% of test months moved by 0.2 points or less.
- A standard time-series model didn't help: ARIMA's average error was 0.305, against 0.304 for the simple guess. Ridge reached 0.277, about 9% lower, but that could still be luck (p = 0.13).
- A standard time-series model didn't help: ARIMA's average error was 0.305, against 0.304 for the simple guess. Ridge reached 0.277, about 9% lower, but that could still be luck (p = 0.13).

## How it was tested

Each month is forecast using only earlier months, so the models never see the future.
The data uses current published figures, so it ignores any later revisions.

## Run it yourself

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python src/download_data.py
    python src/prepare_data.py
    python src/compare.py
    python src/forecast.py

Note that src/download_data.py fetches the latest data, so your numbers may differ.

## Data

- UK CPI annual rate (D7G7): Office for National Statistics
- Brent crude oil price (MCOILBRENTEU) and US dollars per pound (EXUSUK): FRED
