"""Downloads the raw data and saves it in data/raw"""

from pathlib import Path 

import requests 

RAW_FOLDER = Path("data/raw")

SOURCES = {
    "cpi_rate.csv": "https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7g7/mm23",
    "brent_oil.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MCOILBRENTEU",
    "usd_per_gbp.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXUSUK"
} 

def download_all():
    RAW_FOLDER.mkdir(parents=True, exist_ok=True)
    for file_name, url in SOURCES.items():
        response = requests.get(url, timeout =30)
        response.raise_for_status()
        (RAW_FOLDER / file_name).write_bytes(response.content)
        print(f"Saved {file_name} ({len(response.content):,} bytes)")

if __name__ == "__main__":
    download_all()

