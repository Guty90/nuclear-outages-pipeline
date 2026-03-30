import os
import pandas as pd

FILES = {
    "FACILITIES":        "data/processed/facilities.parquet",
    "FACILITY OUTAGES":  "data/processed/facility_outages_clean.parquet",
    "GENERATOR OUTAGES": "data/processed/generator_outages_clean.parquet",
}

for name, path in FILES.items():
    print(f"\n=== {name} ===")

    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue

    df = pd.read_parquet(path)
    print(f"Rows: {len(df)}")
    print(df.head())
    print(df.dtypes)