# Nordic Infra Sustainability — v0.9

**One‑liner:** Energy, CO2e, delay and cost by city (CPH/STH/OSL) with an executive view and a What‑if page.

## Problem
Executives need a single place to compare energy/CO2e vs plan and understand delays/cost per city/asset.

## Dataset (synthetic)
- `DimDate`, `DimLocation`, `DimAsset`, `DimMetric`; `FactMeasurements` with `PlanValue` and `ActualValue`.
- Generated with `/python/generate_synthetic_data.py` (seeded). See **Data dictionary**.

## Star schema
![model](/assets/thumbnails/model-star.png)  
See `/docs/model-star.mmd` for Mermaid source.

## KPIs
- Energy (kWh), CO2e (t), Delay (days), Cost (local), Cost per kWh, Variance % (plan vs actual).

## DAX measures
See `/measures/DAX.md` for full list (base measures, metric‑scoped, YTD/MTD/QTD).

## How to run
1) Clone repo. 2) Run `python/python -m pip install -r python/requirements.txt` (optional).
3) Run `python/generate_synthetic_data.py` to (re)generate CSVs in `/data/synthetic/`.
4) Open the PBIX, connect to `/data/synthetic/*.csv`. 
5) Mark `DimDate[Date]` as date table. Validate relationships (single direction). 6) Export one‑pager PDF.

## Business so‑what
Faster variance detection at city/asset level; supports scenario analysis via slider.

## Limitations
Synthetic data only; Fabric/Dataflows optional; costs shown in a single local currency.

**Demo pack**
- [One-pager (PDF)](media/one-pager_v0.9_en.pdf)
- [GIF 90s](media/demo-90s_v0.9.gif)

## Roadmap to v1.0
- Add accessibility checks, refine What‑if, publish to Service and document refresh.

## License
Code under MIT, data under CC BY 4.0.