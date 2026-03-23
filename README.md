# 📊 Sales Performance Analytics Project

> **End-to-end sales analytics pipeline using SQL · Python · Excel · Power BI**  
> Dataset: 5,000 orders · 2022–2024 · 10 Sales Reps · 5 Regions · 5 Categories

---

## 📁 Project Structure

```
sales-performance-project/
├── data/
│   ├── sales_raw.csv              # 5,000 synthetic sales records
│   ├── sales.db                   # SQLite database
│   ├── schema.json                # Column data types
│   └── sql_results/               # 10 CSV exports from SQL queries
│       ├── 01_revenue_by_year.csv
│       ├── 02_revenue_by_region.csv
│       ├── 03_revenue_by_category.csv
│       ├── 04_top10_products.csv
│       ├── 05_sales_rep_performance.csv
│       ├── 06_monthly_trend.csv
│       ├── 07_channel_analysis.csv
│       ├── 08_order_status_summary.csv
│       ├── 09_quarterly_growth.csv
│       └── 10_high_value_orders.csv
│
├── sql/
│   └── sales_analysis.sql         # 17 SQL queries (schema + analytics)
│
├── python/
│   ├── 01_generate_data.py        # Synthetic dataset generator
│   ├── 02_sql_analysis.py         # SQLite query runner + CSV export
│   ├── 03_eda_visualizations.py   # 8 Matplotlib/Seaborn charts
│   ├── 04_excel_report.py         # openpyxl Excel report builder
│   └── charts/                    # Generated PNG charts
│       ├── 01_monthly_trend.png
│       ├── 02_revenue_by_region.png
│       ├── 03_category_donut.png
│       ├── 04_sales_rep_performance.png
│       ├── 05_margin_distribution.png
│       ├── 06_quarterly_growth.png
│       ├── 07_channel_category_heatmap.png
│       └── 08_order_status.png
│
├── excel/
│   └── Sales_Performance_Report.xlsx   # 5-sheet Excel workbook
│
├── powerbi/
│   └── PowerBI_Setup_DAX_Guide.md      # Full DAX measures + setup guide
│
├── logs/                               # Execution logs per script
│   ├── 01_generate_data.log
│   ├── 02_sql_analysis.log
│   ├── 03_eda_visualizations.log
│   └── 04_excel_report.log
│
├── docs/
│   └── project_summary.md              # Key findings & insights
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Full Pipeline
```bash
# Step 1 — Generate synthetic data (5,000 records)
python python/01_generate_data.py

# Step 2 — Run SQL analysis (17 queries → 10 CSV exports)
python python/02_sql_analysis.py

# Step 3 — EDA + 8 visualizations
python python/03_eda_visualizations.py

# Step 4 — Build Excel report (5 sheets + charts)
python python/04_excel_report.py
```

---

## 📊 Dataset Schema

| Column         | Type    | Description                        |
|----------------|---------|------------------------------------|
| order_id       | TEXT    | Unique order identifier            |
| order_date     | DATE    | Date order was placed              |
| ship_date      | DATE    | Date order was shipped             |
| region         | TEXT    | Sales region (5 regions)           |
| country        | TEXT    | Country within region              |
| sales_rep      | TEXT    | Sales representative name          |
| category       | TEXT    | Product category (5 categories)    |
| product        | TEXT    | Product name (20 products)         |
| channel        | TEXT    | Sales channel (4 channels)         |
| quantity       | INT     | Units ordered                      |
| unit_price     | FLOAT   | Price per unit ($)                 |
| discount       | FLOAT   | Discount rate (0.0–0.25)           |
| gross_revenue  | FLOAT   | quantity × unit_price              |
| net_revenue    | FLOAT   | gross_revenue × (1 - discount)     |
| cogs           | FLOAT   | Cost of goods sold                 |
| profit         | FLOAT   | net_revenue − cogs                 |
| profit_margin  | FLOAT   | profit / net_revenue               |
| status         | TEXT    | Completed / Pending / Cancelled / Returned |
| days_to_ship   | INT     | Fulfillment time (days)            |

---

## 📈 Key Results

| KPI                  | Value          |
|----------------------|----------------|
| Total Revenue        | $225.8M        |
| Total Profit         | $118.9M        |
| Avg Profit Margin    | 52.6%          |
| Total Orders         | 3,954 (completed) |
| Avg Order Value      | $57,118        |
| Top Region           | Asia-Pacific   |
| Top Category         | Consulting     |
| Top Sales Rep        | Bob Martinez   |
| YoY Revenue Growth   | +7.5% (2023→2024) |
| Order Completion Rate| 79.1%          |

---

## 🗄️ SQL Highlights

17 queries covering:
- **Revenue Trends** — Yearly, quarterly, monthly aggregations
- **Regional Analysis** — Revenue share by region with % of total
- **Product Ranking** — Top 10 products, category breakdown
- **Rep Performance** — Leaderboard, quarterly trend, Dense Rank window function
- **Channel Analytics** — Discount impact, channel × category cross-tab
- **Operational Metrics** — Days to ship, order status funnel, revenue at risk
- **Advanced Analytics** — Running totals, YoY growth, MoM growth (window functions)

---

## 🐍 Python Stack

| Library       | Usage                               |
|---------------|-------------------------------------|
| pandas        | Data manipulation & aggregation     |
| numpy         | Numerical operations                |
| matplotlib    | Custom chart generation             |
| seaborn       | Statistical visualizations          |
| openpyxl      | Excel workbook creation             |
| sqlite3       | SQL query execution                 |
| logging       | Execution audit trail               |

---

## 📗 Excel Report Sheets

| Sheet                | Content                                      |
|----------------------|----------------------------------------------|
| Executive Dashboard  | KPI cards + yearly + region summary tables   |
| Raw Data             | 500-row sample of the dataset                |
| Category Analysis    | Revenue by category + embedded bar chart     |
| Rep Leaderboard      | Top reps with medals + horizontal bar chart  |
| Channel Analysis     | Revenue & margin by sales channel            |

---

## 📊 Power BI

The `powerbi/PowerBI_Setup_DAX_Guide.md` contains:
- Step-by-step data import instructions
- M Language code for DimDate table
- **25+ DAX measures** (KPIs, time intelligence, rankings, advanced)
- Recommended visual layout for 4 dashboard pages
- Publishing & sharing guidance

---

## 🔑 Key Insights

1. **Consistent Growth** — Revenue grew from $71M (2022) → $78M (2024), +10.1% overall
2. **Asia-Pacific Leads** — Largest region at 20.9% revenue share
3. **Consulting is King** — Highest revenue category; also highest avg order value
4. **Online Channel** — Highest volume (1,049 orders) with low 5% avg discount
5. **Partner Channel** — Highest avg discount (17.8%) yet competitive margins
6. **Margin Stability** — All categories maintain ~52–53% profit margin (healthy & consistent)
7. **Fulfillment** — Avg 7.5 days to ship; Direct Sales fastest channel
8. **Revenue at Risk** — ~21% of orders (Pending/Cancelled/Returned) worth $57M

---

## 📋 Requirements

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
```

---

## 📝 License

MIT License — free to use, modify, and distribute.

---

*Built with Python 3.12 · SQLite 3.45 · openpyxl 3.1 · Matplotlib 3.8*
