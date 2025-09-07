# DAX Measures (base)

## Date table
```DAX
Date =
ADDCOLUMNS(
  CALENDAR(DATE(2024,1,1), DATE(2025,12,31)),
  "DateKey", VALUE(FORMAT([Date], "YYYYMMDD")),
  "Year", YEAR([Date]),
  "Month", MONTH([Date]),
  "MonthName", FORMAT([Date], "MMM"),
  "Quarter", "Q" & FORMAT(ROUNDUP(MONTH([Date])/3,0), "0"),
  "YearMonth", FORMAT([Date], "YYYY-MM"),
  "YearMonthNum", YEAR([Date]) * 100 + MONTH([Date]),
  "MonthSort", MONTH([Date])
)

```
> Mark `Date[Date]` as date table. Disable Auto Date/Time.

## Base
```DAX
ValueActual := SUM('fact_measurements'[ActualValue])
ValuePlan   := SUM('fact_measurements'[PlanValue])
Variance    := [ValueActual] - [ValuePlan]
VariancePct := DIVIDE([Variance], [ValuePlan], 0)
```

## Metric-scoped (uses `dim_metric[MetricCode]`)
```DAX
EnergyActualKWh := CALCULATE([ValueActual], 'dim_metric'[MetricCode] = "ENERGY_KWH")
EnergyPlanKWh   := CALCULATE([ValuePlan],   'dim_metric'[MetricCode] = "ENERGY_KWH")
EnergyVarPct    := DIVIDE([EnergyActualKWh] - [EnergyPlanKWh], [EnergyPlanKWh])

CO2eActualT     := CALCULATE([ValueActual], 'dim_metric'[MetricCode] = "CO2E_T")
CostActualLocal := CALCULATE([ValueActual], 'dim_metric'[MetricCode] = "COST_LOCAL")
DelayDays       := CALCULATE([ValueActual], 'dim_metric'[MetricCode] = "DELAY_DAYS")

CostPerKWh        := DIVIDE([CostActualLocal], [EnergyActualKWh])
```

## Time‑intelligence
```DAX
EnergyYTDKWh := TOTALYTD([EnergyActualKWh], 'Date'[Date])
EnergyMTDKWh := TOTALMTD([EnergyActualKWh], 'Date'[Date])
EnergyQTDKWh := TOTALQTD([EnergyActualKWh], 'Date'[Date])

CO2eYTDT     := TOTALYTD([CO2eActualT], 'Date'[Date])
CO2eMTDT     := TOTALMTD([CO2eActualT], 'Date'[Date])
CO2eQTDT     := TOTALQTD([CO2eActualT], 'Date'[Date])

CostYTDLocal  := TOTALYTD([CostActualLocal], 'Date'[Date])
CostMTDLocal  := TOTALMTD([CostActualLocal], 'Date'[Date])
CostQTDLocal  := TOTALQTD([CostActualLocal], 'Date'[Date])

DelayYTDDays  := TOTALYTD([DelayDays], 'Date'[Date])
DelayMTDDays  := TOTALMTD([DelayDays], 'Date'[Date])
DelayQTDDays  := TOTALQTD([DelayDays], 'Date'[Date])
```
## What-if (uses energy adjustment parameter `EnergyAdj = GENERATESERIES(0.8, 1.2, 0.02)`)
```DAX
EnergyAdjActualKWh = [EnergyActualKWh] * SELECTEDVALUE(EnergyAdj[EnergyAdj], 1)

EnergyAdjVarPct = DIVIDE([EnergyAdjActualKWh] - [EnergyPlanKWh], [EnergyPlanKWh])
```