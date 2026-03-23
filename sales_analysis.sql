-- =============================================================================
-- SALES PERFORMANCE PROJECT — SQL SCRIPTS
-- Database: SQLite (compatible with PostgreSQL / MySQL with minor adjustments)
-- =============================================================================

-- =============================================================================
-- 1. SCHEMA CREATION
-- =============================================================================

CREATE TABLE IF NOT EXISTS sales (
    order_id        TEXT        PRIMARY KEY,
    order_date      DATE        NOT NULL,
    ship_date       DATE,
    region          TEXT        NOT NULL,
    country         TEXT,
    sales_rep       TEXT        NOT NULL,
    category        TEXT        NOT NULL,
    product         TEXT        NOT NULL,
    channel         TEXT        NOT NULL,
    quantity        INTEGER     NOT NULL,
    unit_price      REAL        NOT NULL,
    discount        REAL        DEFAULT 0,
    gross_revenue   REAL,
    net_revenue     REAL,
    cogs            REAL,
    profit          REAL,
    profit_margin   REAL,
    status          TEXT        NOT NULL,
    days_to_ship    INTEGER
);

CREATE INDEX IF NOT EXISTS idx_sales_date     ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_sales_region   ON sales(region);
CREATE INDEX IF NOT EXISTS idx_sales_rep      ON sales(sales_rep);
CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category);
CREATE INDEX IF NOT EXISTS idx_sales_status   ON sales(status);


-- =============================================================================
-- 2. REVENUE PERFORMANCE QUERIES
-- =============================================================================

-- Q1: Yearly Revenue & Profit Summary
SELECT
    strftime('%Y', order_date)          AS year,
    COUNT(*)                             AS total_orders,
    ROUND(SUM(net_revenue), 2)           AS total_revenue,
    ROUND(SUM(profit), 2)                AS total_profit,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct
FROM sales
WHERE status = 'Completed'
GROUP BY year
ORDER BY year;


-- Q2: Monthly Revenue Trend (for time-series charts)
SELECT
    strftime('%Y-%m', order_date)        AS month,
    COUNT(*)                             AS orders,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    ROUND(SUM(profit), 2)                AS profit,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct
FROM sales
WHERE status = 'Completed'
GROUP BY month
ORDER BY month;


-- Q3: Quarterly Growth Analysis with YoY Change
WITH quarterly AS (
    SELECT
        strftime('%Y', order_date)                           AS year,
        CAST(((strftime('%m', order_date) - 1) / 3) + 1 AS INT) AS quarter,
        ROUND(SUM(net_revenue), 2)                           AS revenue,
        ROUND(SUM(profit), 2)                                AS profit
    FROM sales
    WHERE status = 'Completed'
    GROUP BY year, quarter
)
SELECT
    q.year,
    q.quarter,
    q.revenue,
    q.profit,
    prev.revenue                               AS prev_year_revenue,
    ROUND((q.revenue - prev.revenue) / prev.revenue * 100, 2) AS yoy_growth_pct
FROM quarterly q
LEFT JOIN quarterly prev
    ON q.quarter = prev.quarter
    AND CAST(q.year AS INT) = CAST(prev.year AS INT) + 1
ORDER BY q.year, q.quarter;


-- =============================================================================
-- 3. REGIONAL & PRODUCT ANALYSIS
-- =============================================================================

-- Q4: Revenue by Region
SELECT
    region,
    COUNT(*)                             AS orders,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    ROUND(SUM(profit), 2)                AS profit,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct,
    ROUND(SUM(net_revenue) * 100.0 /
          (SELECT SUM(net_revenue) FROM sales WHERE status='Completed'), 2) AS revenue_share_pct
FROM sales
WHERE status = 'Completed'
GROUP BY region
ORDER BY revenue DESC;


-- Q5: Top 10 Products by Revenue
SELECT
    product,
    category,
    COUNT(*)                             AS orders,
    SUM(quantity)                        AS units_sold,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    ROUND(SUM(profit), 2)                AS profit,
    ROUND(AVG(unit_price), 2)            AS avg_unit_price,
    ROUND(AVG(discount) * 100, 2)        AS avg_discount_pct
FROM sales
WHERE status = 'Completed'
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;


-- Q6: Category Revenue Breakdown
SELECT
    category,
    COUNT(*)                             AS orders,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    ROUND(SUM(profit), 2)                AS profit,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct
FROM sales
WHERE status = 'Completed'
GROUP BY category
ORDER BY revenue DESC;


-- =============================================================================
-- 4. SALES REP PERFORMANCE
-- =============================================================================

-- Q7: Sales Rep Leaderboard
SELECT
    sales_rep,
    COUNT(*)                             AS total_orders,
    ROUND(SUM(net_revenue), 2)           AS total_revenue,
    ROUND(SUM(profit), 2)                AS total_profit,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct,
    ROUND(SUM(net_revenue) / COUNT(*), 2) AS avg_order_value,
    MIN(order_date)                       AS first_sale,
    MAX(order_date)                       AS last_sale
FROM sales
WHERE status = 'Completed'
GROUP BY sales_rep
ORDER BY total_revenue DESC;


-- Q8: Sales Rep Performance by Quarter (Trend)
SELECT
    sales_rep,
    strftime('%Y', order_date)            AS year,
    CAST(((strftime('%m', order_date)-1)/3)+1 AS INT) AS quarter,
    COUNT(*)                              AS orders,
    ROUND(SUM(net_revenue), 2)            AS revenue
FROM sales
WHERE status = 'Completed'
GROUP BY sales_rep, year, quarter
ORDER BY sales_rep, year, quarter;


-- =============================================================================
-- 5. CHANNEL ANALYSIS
-- =============================================================================

-- Q9: Channel Performance
SELECT
    channel,
    COUNT(*)                             AS orders,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    ROUND(SUM(profit), 2)                AS profit,
    ROUND(AVG(discount) * 100, 2)        AS avg_discount_pct,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct,
    ROUND(SUM(net_revenue) / COUNT(*), 2) AS avg_order_value
FROM sales
WHERE status = 'Completed'
GROUP BY channel
ORDER BY revenue DESC;


-- Q10: Channel × Category Cross-Tab (Pivot-ready)
SELECT
    channel,
    category,
    COUNT(*)                             AS orders,
    ROUND(SUM(net_revenue), 2)           AS revenue
FROM sales
WHERE status = 'Completed'
GROUP BY channel, category
ORDER BY channel, revenue DESC;


-- =============================================================================
-- 6. OPERATIONAL METRICS
-- =============================================================================

-- Q11: Order Status Funnel & Revenue at Risk
SELECT
    status,
    COUNT(*)                             AS order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 2) AS pct_of_total,
    ROUND(SUM(net_revenue), 2)           AS revenue_value
FROM sales
GROUP BY status
ORDER BY order_count DESC;


-- Q12: Average Days to Ship by Channel
SELECT
    channel,
    ROUND(AVG(days_to_ship), 1)          AS avg_days_to_ship,
    MIN(days_to_ship)                    AS min_days,
    MAX(days_to_ship)                    AS max_days,
    COUNT(*)                             AS total_orders
FROM sales
WHERE status = 'Completed'
GROUP BY channel
ORDER BY avg_days_to_ship;


-- Q13: High-Value Orders (>$50K)
SELECT
    order_id, order_date, sales_rep, product, region,
    ROUND(net_revenue, 2)               AS net_revenue,
    ROUND(profit, 2)                    AS profit,
    ROUND(profit_margin * 100, 2)       AS margin_pct,
    status
FROM sales
WHERE net_revenue > 50000
ORDER BY net_revenue DESC
LIMIT 25;


-- Q14: Discount Impact on Profit Margin
SELECT
    CASE
        WHEN discount = 0          THEN '0% — No Discount'
        WHEN discount <= 0.05      THEN '1–5%'
        WHEN discount <= 0.10      THEN '6–10%'
        WHEN discount <= 0.20      THEN '11–20%'
        ELSE '21%+'
    END                                  AS discount_tier,
    COUNT(*)                             AS orders,
    ROUND(AVG(profit_margin) * 100, 2)   AS avg_margin_pct,
    ROUND(SUM(net_revenue), 2)           AS total_revenue
FROM sales
WHERE status = 'Completed'
GROUP BY discount_tier
ORDER BY MIN(discount);


-- =============================================================================
-- 7. ADVANCED ANALYTICS
-- =============================================================================

-- Q15: Running Revenue Total by Month (Window Function — PostgreSQL / MySQL 8+)
-- Note: SQLite supports window functions since version 3.25 (2018)
SELECT
    strftime('%Y-%m', order_date)        AS month,
    ROUND(SUM(net_revenue), 2)           AS monthly_revenue,
    ROUND(SUM(SUM(net_revenue)) OVER (
        ORDER BY strftime('%Y-%m', order_date)
    ), 2)                                AS cumulative_revenue
FROM sales
WHERE status = 'Completed'
GROUP BY month
ORDER BY month;


-- Q16: Rep Revenue Rank per Year (Dense Rank)
SELECT
    strftime('%Y', order_date)           AS year,
    sales_rep,
    ROUND(SUM(net_revenue), 2)           AS revenue,
    DENSE_RANK() OVER (
        PARTITION BY strftime('%Y', order_date)
        ORDER BY SUM(net_revenue) DESC
    )                                    AS rank_in_year
FROM sales
WHERE status = 'Completed'
GROUP BY year, sales_rep
ORDER BY year, rank_in_year;


-- Q17: Month-over-Month Growth Rate
WITH monthly AS (
    SELECT
        strftime('%Y-%m', order_date)    AS month,
        SUM(net_revenue)                 AS revenue
    FROM sales
    WHERE status = 'Completed'
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2)                    AS revenue,
    LAG(revenue) OVER (ORDER BY month)   AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) /
          LAG(revenue) OVER (ORDER BY month) * 100, 2) AS mom_growth_pct
FROM monthly
ORDER BY month;
