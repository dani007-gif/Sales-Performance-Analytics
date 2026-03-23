"""
Sales Performance Project
Step 2: SQL Analysis via SQLite
"""

import sqlite3
import pandas as pd
import logging
import os
import json

os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("../logs/02_sql_analysis.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── Load CSV → SQLite ─────────────────────────────────────────────────────────
df = pd.read_csv("../data/sales_raw.csv")
conn = sqlite3.connect("../data/sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
log.info("Loaded %d rows into SQLite table 'sales'", len(df))

# ── SQL Queries ───────────────────────────────────────────────────────────────
QUERIES = {
    "01_revenue_by_year": """
        SELECT
            strftime('%Y', order_date)          AS year,
            COUNT(*)                             AS total_orders,
            SUM(net_revenue)                     AS total_revenue,
            SUM(profit)                          AS total_profit,
            ROUND(AVG(profit_margin)*100, 2)     AS avg_margin_pct
        FROM sales
        WHERE status = 'Completed'
        GROUP BY year
        ORDER BY year;
    """,
    "02_revenue_by_region": """
        SELECT
            region,
            COUNT(*)                             AS orders,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(SUM(profit),2)                 AS profit,
            ROUND(AVG(profit_margin)*100,2)      AS avg_margin_pct
        FROM sales
        WHERE status = 'Completed'
        GROUP BY region
        ORDER BY revenue DESC;
    """,
    "03_revenue_by_category": """
        SELECT
            category,
            COUNT(*)                             AS orders,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(SUM(profit),2)                 AS profit,
            ROUND(AVG(profit_margin)*100,2)      AS avg_margin_pct
        FROM sales
        WHERE status = 'Completed'
        GROUP BY category
        ORDER BY revenue DESC;
    """,
    "04_top10_products": """
        SELECT
            product,
            category,
            COUNT(*)                             AS orders,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(SUM(profit),2)                 AS profit
        FROM sales
        WHERE status = 'Completed'
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 10;
    """,
    "05_sales_rep_performance": """
        SELECT
            sales_rep,
            COUNT(*)                             AS total_orders,
            ROUND(SUM(net_revenue),2)            AS total_revenue,
            ROUND(SUM(profit),2)                 AS total_profit,
            ROUND(AVG(profit_margin)*100,2)      AS avg_margin_pct,
            ROUND(SUM(net_revenue)/COUNT(*),2)   AS avg_order_value
        FROM sales
        WHERE status = 'Completed'
        GROUP BY sales_rep
        ORDER BY total_revenue DESC;
    """,
    "06_monthly_trend": """
        SELECT
            strftime('%Y-%m', order_date)        AS month,
            COUNT(*)                             AS orders,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(SUM(profit),2)                 AS profit
        FROM sales
        WHERE status = 'Completed'
        GROUP BY month
        ORDER BY month;
    """,
    "07_channel_analysis": """
        SELECT
            channel,
            COUNT(*)                             AS orders,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(AVG(discount)*100,2)           AS avg_discount_pct,
            ROUND(AVG(profit_margin)*100,2)      AS avg_margin_pct
        FROM sales
        WHERE status = 'Completed'
        GROUP BY channel
        ORDER BY revenue DESC;
    """,
    "08_order_status_summary": """
        SELECT
            status,
            COUNT(*)                             AS count,
            ROUND(SUM(net_revenue),2)            AS revenue_at_risk
        FROM sales
        GROUP BY status
        ORDER BY count DESC;
    """,
    "09_quarterly_growth": """
        SELECT
            strftime('%Y', order_date)           AS year,
            CAST(((strftime('%m', order_date)-1)/3)+1 AS INT) AS quarter,
            ROUND(SUM(net_revenue),2)            AS revenue,
            ROUND(SUM(profit),2)                 AS profit
        FROM sales
        WHERE status = 'Completed'
        GROUP BY year, quarter
        ORDER BY year, quarter;
    """,
    "10_high_value_orders": """
        SELECT order_id, order_date, sales_rep, product, region,
               net_revenue, profit, profit_margin, status
        FROM sales
        WHERE net_revenue > 50000
        ORDER BY net_revenue DESC
        LIMIT 20;
    """,
}

results = {}
os.makedirs("../data/sql_results", exist_ok=True)

for name, sql in QUERIES.items():
    result_df = pd.read_sql_query(sql, conn)
    results[name] = result_df
    out_path = f"../data/sql_results/{name}.csv"
    result_df.to_csv(out_path, index=False)
    log.info("Query %-35s → %d rows saved to %s", name, len(result_df), out_path)

conn.close()
log.info("All SQL queries complete. Results in ../data/sql_results/")

# Print key results
print("\n" + "="*60)
print("REVENUE BY YEAR")
print("="*60)
print(results["01_revenue_by_year"].to_string(index=False))

print("\n" + "="*60)
print("REVENUE BY REGION")
print("="*60)
print(results["02_revenue_by_region"].to_string(index=False))

print("\n" + "="*60)
print("TOP SALES REPS")
print("="*60)
print(results["05_sales_rep_performance"].to_string(index=False))

print("\n" + "="*60)
print("CHANNEL ANALYSIS")
print("="*60)
print(results["07_channel_analysis"].to_string(index=False))
