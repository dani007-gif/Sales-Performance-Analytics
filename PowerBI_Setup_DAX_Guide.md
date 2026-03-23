# Power BI — Sales Performance Dashboard
## Setup Guide & DAX Measures Reference

---

## 1. Data Import

### Connect to SQLite / CSV
1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Navigate to `data/sales_raw.csv` → Load
3. In Power Query Editor, verify column types:
   - `order_date`, `ship_date` → **Date**
   - `net_revenue`, `profit`, `cogs`, `unit_price` → **Decimal Number**
   - `quantity`, `days_to_ship` → **Whole Number**
   - All others → **Text**
4. Click **Close & Apply**

---

## 2. Data Model

### Fact Table
| Table  | Column        | Type    |
|--------|---------------|---------|
| sales  | order_id      | Text PK |
| sales  | order_date    | Date    |
| sales  | net_revenue   | Decimal |
| sales  | profit        | Decimal |
| sales  | status        | Text    |
| ...    | ...           | ...     |

### Recommended Dimension Tables (create via Power Query)
- **DimDate** — Full calendar table (year, quarter, month, week)
- **DimRegion** — region, country
- **DimProduct** — product, category
- **DimRep** — sales_rep, region

### Create Date Table in Power Query (M Language)
```m
let
    StartDate = #date(2022, 1, 1),
    EndDate   = #date(2024, 12, 31),
    DayCount  = Duration.Days(EndDate - StartDate) + 1,
    Source    = List.Dates(StartDate, DayCount, #duration(1,0,0,0)),
    Table     = Table.FromList(Source, Splitter.SplitByNothing()),
    DateCol   = Table.RenameColumns(Table, {{"Column1", "Date"}}),
    WithYear  = Table.AddColumn(DateCol, "Year", each Date.Year([Date]), Int64.Type),
    WithQtr   = Table.AddColumn(WithYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date]))),
    WithMonth = Table.AddColumn(WithQtr, "Month", each Date.Month([Date]), Int64.Type),
    WithMonthName = Table.AddColumn(WithMonth, "MonthName", each Date.ToText([Date], "MMM")),
    WithWeek  = Table.AddColumn(WithMonthName, "WeekNo", each Date.WeekOfYear([Date]), Int64.Type)
in
    WithWeek
```

---

## 3. DAX Measures

Paste all measures into a **_Measures** table in your model.

### ── KPI Measures ──

```dax
Total Revenue =
CALCULATE(
    SUM(sales[net_revenue]),
    sales[status] = "Completed"
)

Total Profit =
CALCULATE(
    SUM(sales[profit]),
    sales[status] = "Completed"
)

Total Orders =
CALCULATE(
    COUNTROWS(sales),
    sales[status] = "Completed"
)

Avg Order Value =
DIVIDE([Total Revenue], [Total Orders], 0)

Avg Profit Margin % =
CALCULATE(
    AVERAGE(sales[profit_margin]),
    sales[status] = "Completed"
) * 100

Gross Revenue =
CALCULATE(
    SUM(sales[gross_revenue]),
    sales[status] = "Completed"
)

Total Discount Amount =
[Gross Revenue] - [Total Revenue]

Avg Discount % =
CALCULATE(
    AVERAGE(sales[discount]),
    sales[status] = "Completed"
) * 100
```

### ── Time Intelligence ──

```dax
Revenue PY =
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(DimDate[Date])
)

Revenue YoY Growth % =
DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY], 0) * 100

Revenue YTD =
TOTALYTD(
    [Total Revenue],
    DimDate[Date]
)

Revenue QTD =
TOTALQTD(
    [Total Revenue],
    DimDate[Date]
)

Revenue MTD =
TOTALMTD(
    [Total Revenue],
    DimDate[Date]
)

Running Total Revenue =
CALCULATE(
    [Total Revenue],
    FILTER(
        ALL(DimDate[Date]),
        DimDate[Date] <= MAX(DimDate[Date])
    )
)

3-Month Rolling Revenue =
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -3, MONTH)
)
```

### ── Rankings ──

```dax
Rep Revenue Rank =
RANKX(
    ALL(sales[sales_rep]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)

Region Revenue Rank =
RANKX(
    ALL(sales[region]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)

Category Revenue Rank =
RANKX(
    ALL(sales[category]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)
```

### ── Advanced Calculations ──

```dax
Revenue Share % =
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(sales)),
    0
) * 100

Profit Margin Band =
SWITCH(
    TRUE(),
    [Avg Profit Margin %] >= 60, "High (60%+)",
    [Avg Profit Margin %] >= 45, "Medium (45–60%)",
    [Avg Profit Margin %] >= 30, "Low (30–45%)",
    "Very Low (<30%)"
)

Orders at Risk =
CALCULATE(
    COUNTROWS(sales),
    sales[status] IN {"Pending", "Cancelled", "Returned"}
)

Revenue at Risk =
CALCULATE(
    SUM(sales[net_revenue]),
    sales[status] IN {"Pending", "Cancelled", "Returned"}
)

Win Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(sales), sales[status] = "Completed"),
    COUNTROWS(sales),
    0
) * 100

Avg Days to Ship =
CALCULATE(
    AVERAGE(sales[days_to_ship]),
    sales[status] = "Completed"
)
```

---

## 4. Recommended Visuals Layout

### Page 1 — Executive Summary
| Visual         | Fields                                      |
|----------------|---------------------------------------------|
| Card           | Total Revenue, Total Profit, Avg Margin %   |
| Card           | Total Orders, Win Rate %, Avg Order Value   |
| Line Chart     | Revenue & Profit by Month (DimDate)         |
| Bar Chart      | Revenue by Region                           |
| Donut Chart    | Revenue Share by Category                   |
| Slicer         | Year, Quarter, Region                       |

### Page 2 — Sales Rep Performance
| Visual         | Fields                                      |
|----------------|---------------------------------------------|
| Table/Matrix   | Rep, Orders, Revenue, Profit, Margin %, Rank|
| Bar Chart      | Revenue by Rep (sorted desc)                |
| Scatter Plot   | Orders vs Revenue (bubble = margin %)        |
| Line Chart     | Rep Revenue Trend by Quarter                |

### Page 3 — Product & Channel
| Visual         | Fields                                      |
|----------------|---------------------------------------------|
| Bar Chart      | Top 10 Products by Revenue                  |
| Matrix         | Channel × Category Revenue                  |
| Gauge          | Avg Discount % vs Target                    |
| Bar Chart      | Avg Days to Ship by Channel                 |

### Page 4 — Time Intelligence
| Visual         | Fields                                      |
|----------------|---------------------------------------------|
| Line Chart     | Revenue YTD vs Revenue PY                   |
| Column Chart   | Quarterly Revenue with YoY Growth %         |
| KPI Card       | Revenue YoY Growth %                        |
| Area Chart     | Running Total Revenue                       |

---

## 5. Formatting Tips
- Use **dark theme** (View → Themes → Executive) for premium look
- Apply **conditional formatting** on margin columns (green/red)
- Add **tooltips pages** for drill-through detail
- Set **cross-filter** behavior between all visuals on a page
- Use **bookmarks** for different time period views (YTD / QTD / MTD)
- Enable **Row-Level Security** if sharing across teams

---

## 6. Publishing
1. File → Publish → **My Workspace** (or target workspace)
2. Set **scheduled refresh** if connecting to live database
3. Share dashboard link with stakeholders
4. Export PDF: File → Export → PDF

---

*Generated by Sales Performance Project | 2022–2024 Dataset*
