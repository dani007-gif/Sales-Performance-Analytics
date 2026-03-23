"""
Sales Performance Project
Step 1: Generate synthetic sales dataset from the scratch
"""

import pandas as pd
import numpy as np
import os
import logging
import sys
import json
from datetime import datetime, timedelta
import random

# ── Logging ──────────────────────────────────────────────────────────────────
os.makedirs("../logs", exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("../logs/01_generate_data.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

N_ROWS = 5_000
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2024, 12, 31)

REGIONS = ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"]
CATEGORIES = ["Electronics", "Software", "Consulting", "Hardware", "Services"]
CHANNELS = ["Online", "Direct Sales", "Partner", "Retail"]

PRODUCTS = {
    "Electronics": ["Laptop Pro", "Tablet X", "Smart Monitor", "Headphones Elite"],
    "Software":    ["CRM Suite", "Analytics Cloud", "ERP Platform", "Security Suite"],
    "Consulting":  ["IT Strategy", "Digital Transform", "Cloud Migration", "Data Audit"],
    "Hardware":    ["Server Rack", "Network Switch", "Storage Array", "UPS System"],
    "Services":    ["Support Plus", "Managed Services", "Training Bundle", "SLA Gold"],
}

SALESREPS = [
    "Alice Johnson", "Bob Martinez", "Carol Smith", "David Lee",
    "Emma Wilson", "Frank Brown", "Grace Kim", "Henry Davis",
    "Iris Chen", "James Taylor",
]

PRICE_RANGE = {
    "Electronics": (300, 3500),
    "Software":    (500, 8000),
    "Consulting":  (2000, 25000),
    "Hardware":    (1000, 15000),
    "Services":    (200, 5000),
}

DISCOUNT_RANGE = {
    "Online":       (0.00, 0.10),
    "Direct Sales": (0.05, 0.20),
    "Partner":      (0.10, 0.25),
    "Retail":       (0.00, 0.08),
}

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def build_record(_):
    region   = random.choice(REGIONS)
    category = random.choice(CATEGORIES)
    product  = random.choice(PRODUCTS[category])
    channel  = random.choice(CHANNELS)
    rep      = random.choice(SALESREPS)
    qty      = random.randint(1, 20)
    unit_price = round(random.uniform(*PRICE_RANGE[category]), 2)
    discount   = round(random.uniform(*DISCOUNT_RANGE[channel]), 3)
    gross      = round(qty * unit_price, 2)
    net_revenue= round(gross * (1 - discount), 2)
    cogs_pct   = random.uniform(0.30, 0.65)
    cogs       = round(net_revenue * cogs_pct, 2)
    profit     = round(net_revenue - cogs, 2)
    order_date = random_date(START_DATE, END_DATE)
    ship_days  = random.randint(1, 14)
    ship_date  = order_date + timedelta(days=ship_days)
    status     = random.choices(
        ["Completed", "Pending", "Cancelled", "Returned"],
        weights=[0.78, 0.10, 0.07, 0.05],
    )[0]
    return {
        "order_id":    f"ORD-{_+10001}",
        "order_date":  order_date.strftime("%Y-%m-%d"),
        "ship_date":   ship_date.strftime("%Y-%m-%d"),
        "region":      region,
        "country":     f"{region}_Country_{random.randint(1,5)}",
        "sales_rep":   rep,
        "category":    category,
        "product":     product,
        "channel":     channel,
        "quantity":    qty,
        "unit_price":  unit_price,
        "discount":    discount,
        "gross_revenue": gross,
        "net_revenue":   net_revenue,
        "cogs":          cogs,
        "profit":        profit,
        "profit_margin": round(profit / net_revenue, 4) if net_revenue else 0,
        "status":        status,
        "days_to_ship":  ship_days,
    }

log.info("Generating %d sales records …", N_ROWS)
records = [build_record(i) for i in range(N_ROWS)]
df = pd.DataFrame(records)

os.makedirs("../data", exist_ok=True)
csv_path = "../data/sales_raw.csv"
df.to_csv(csv_path, index=False)
log.info("Saved raw CSV  -> %s  (%d rows x %d cols)", csv_path, *df.shape)
log.info("Saved schema   -> ../data/schema.json")
log.info("Date range     : %s to %s", df.order_date.min(), df.order_date.max())
log.info("Total revenue  : $%.0f", df.net_revenue.sum())
log.info("Total profit   : $%.0f", df.profit.sum())
log.info("Avg margin     : %.1f%%", df.profit_margin.mean() * 100)
log.info("Avg margin     : %.1f%%", df.profit_margin.mean() * 100)
log.info("Status counts  :\n%s", df.status.value_counts().to_string())
log.info("DONE — data generation complete.")
