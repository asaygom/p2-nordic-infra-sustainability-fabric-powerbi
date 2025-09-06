# DAX Measures (base)

## Date table
```DAX
Date =
ADDCOLUMNS(
    CALENDAR(DATE(2023,1,1), DATE(2026,12,31)),
    "Year", YEAR([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM"),
    "Quarter", "Q" & FORMAT(ROUNDUP(MONTH([Date])/3,0), "0"),
    "YearMonth", FORMAT([Date], "YYYY-MM")
)
```
> Mark `Date[Date]` as date table. Disable Auto Date/Time.

## Base
```DAX
Value Actual := SUM('FactMeasurements'[ActualValue])
Value Plan   := SUM('FactMeasurements'[PlanValue])
Variance     := [Value Actual] - [Value Plan]
Variance %   := DIVIDE([Variance], [Value Plan])
```

## Metric-scoped (uses `DimMetric[MetricCode]`)
```DAX
Energy | Actual (kWh) := CALCULATE([Value Actual], 'DimMetric'[MetricCode] = "ENERGY_KWH")
Energy | Plan (kWh)   := CALCULATE([Value Plan],   'DimMetric'[MetricCode] = "ENERGY_KWH")
Energy | Variance %   := DIVIDE([Energy | Actual (kWh)] - [Energy | Plan (kWh)], [Energy | Plan (kWh)])

CO2e | Actual (t)     := CALCULATE([Value Actual], 'DimMetric'[MetricCode] = "CO2E_T")

Cost | Actual (Local) := CALCULATE([Value Actual], 'DimMetric'[MetricCode] = "COST_LOCAL")
Cost | per kWh        := DIVIDE([Cost | Actual (Local)], [Energy | Actual (kWh)])

Delay | Days          := CALCULATE([Value Actual], 'DimMetric'[MetricCode] = "DELAY_DAYS")
```

## Time‑intelligence
```DAX
Energy | YTD (kWh) := TOTALYTD([Energy | Actual (kWh)], 'DimDate'[Date])
Energy | MTD (kWh) := TOTALMTD([Energy | Actual (kWh)], 'DimDate'[Date])
Energy | QTD (kWh) := TOTALQTD([Energy | Actual (kWh)], 'DimDate'[Date])

CO2e | YTD (t) := TOTALYTD([CO2e | Actual (t)], 'DimDate'[Date])
```