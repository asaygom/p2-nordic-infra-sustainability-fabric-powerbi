import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date
rng = np.random.default_rng(42)

base = Path(__file__).resolve().parents[1] / "data" / "synthetic"
base.mkdir(parents=True, exist_ok=True)

# DimDate (monthly granularity for lighter fact table)
dates = pd.date_range("2024-01-01", "2025-12-01", freq="MS")
dim_date = pd.DataFrame({
    "DateKey": dates.strftime("%Y%m%d").astype(int),
    "Date": dates,
    "Year": dates.year,
    "Month": dates.month,
    "MonthName": dates.strftime("%b"),
    "Quarter": ("Q" + ((dates.month-1)//3 + 1).astype(str)),
    "YearMonth": dates.strftime("%Y-%m")
})
dim_date.to_csv(base / "dim_date.csv", index=False)

# DimLocation
locations = [
    (1, "CPH", "Copenhagen", "DK"),
    (2, "OSL", "Oslo", "NO"),
    (3, "STH", "Stockholm", "SE"),
]
dim_location = pd.DataFrame(locations, columns=["LocationKey", "LocationCode", "LocationName", "CountryCode"])
dim_location.to_csv(base / "dim_location.csv", index=False)

# DimAsset (3 per city)
assets = []
asset_id = 1
for loc_key, loc_code, _, _ in locations:
    for i in range(1, 4):
        assets.append((asset_id, f"{loc_code}-A{i}", f"Asset {i} {loc_code}", loc_key))
        asset_id += 1
dim_asset = pd.DataFrame(assets, columns=["AssetKey", "AssetCode", "AssetName", "LocationKey"])
dim_asset.to_csv(base / "dim_asset.csv", index=False)

# DimMetric
metrics = [
    (1, "ENERGY_KWH", "Energy (kWh)"),
    (2, "CO2E_T", "CO2e (t)"),
    (3, "COST_LOCAL", "Cost (local)"),
    (4, "DELAY_DAYS", "Delay (days)"),
]
dim_metric = pd.DataFrame(metrics, columns=["MetricKey", "MetricCode", "MetricName"])
dim_metric.to_csv(base / "dim_metric.csv", index=False)

# FactMeasurements (monthly x asset x metric)
rows = []
for _, d in dim_date.iterrows():
    # seasonality factor (energy higher in winter)
    month = int(d["Month"])
    season = 1.15 if month in [12,1,2] else (0.95 if month in [6,7,8] else 1.0)
    for _, a in dim_asset.iterrows():
        loc = dim_location.loc[dim_location["LocationKey"] == a["LocationKey"]].iloc[0]
        loc_factor = {"CPH": 1.0, "OSL": 1.1, "STH": 0.95}[loc["LocationCode"]]
        base_energy = 10000 * loc_factor * season  # kWh plan baseline
        # metrics plan
        plan_energy = base_energy
        plan_co2e = plan_energy * 0.0002  # t
        plan_cost = plan_energy * {"CPH": 0.32, "OSL": 0.34, "STH": 0.30}[loc["LocationCode"]]  # local
        plan_delay = 0.0

        # actuals with random noise
        noise = rng.normal(0, 0.07)  # 7% std
        actual_energy = plan_energy * (1 + noise)
        actual_co2e = actual_energy * 0.0002 * (1 + rng.normal(0, 0.03))
        actual_cost = actual_energy * {"CPH": 0.32, "OSL": 0.34, "STH": 0.30}[loc["LocationCode"]] * (1 + rng.normal(0, 0.05))
        actual_delay = max(0, rng.normal(0.5, 1.0))  # days

        for metric_key, code, _ in metrics:
            if code == "ENERGY_KWH":
                plan, actual = plan_energy, actual_energy
            elif code == "CO2E_T":
                plan, actual = plan_co2e, actual_co2e
            elif code == "COST_LOCAL":
                plan, actual = plan_cost, actual_cost
            elif code == "DELAY_DAYS":
                plan, actual = plan_delay, actual_delay
            rows.append({
                "DateKey": int(d["DateKey"]),
                "LocationKey": int(a["LocationKey"]),
                "AssetKey": int(a["AssetKey"]),
                "MetricKey": int(metric_key),
                "PlanValue": float(plan),
                "ActualValue": float(actual),
            })

fact = pd.DataFrame(rows)
fact.to_csv(base / "fact_measurements.csv", index=False)

print("Synthetic CSVs written to", base)