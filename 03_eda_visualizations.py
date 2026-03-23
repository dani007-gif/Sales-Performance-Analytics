"""
Sales Performance Project
Step 3: Python EDA + Matplotlib/Seaborn Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import logging
import os
import warnings

warnings.filterwarnings("ignore")
os.makedirs("../logs", exist_ok=True)
os.makedirs("../python/charts", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("../logs/03_eda_visualizations.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("../data/sales_raw.csv", parse_dates=["order_date", "ship_date"])
completed = df[df.status == "Completed"].copy()
log.info("Loaded %d rows; %d completed orders", len(df), len(completed))

# ── Color palette ─────────────────────────────────────────────────────────────
COLORS = ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#e94560",
          "#2ec4b6", "#f7b731", "#20bf6b", "#4b7bec", "#fc5c65"]
sns.set_theme(style="darkgrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 130, "axes.titlepad": 12})

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 1 – Revenue & Profit Monthly Trend
# ═══════════════════════════════════════════════════════════════════════════════
monthly = completed.copy()
monthly["month"] = monthly.order_date.dt.to_period("M")
monthly = monthly.groupby("month").agg(revenue=("net_revenue", "sum"),
                                        profit=("profit", "sum")).reset_index()
monthly["month_dt"] = monthly.month.dt.to_timestamp()

fig, ax1 = plt.subplots(figsize=(14, 5))
ax1.fill_between(monthly.month_dt, monthly.revenue / 1e6, alpha=0.35, color="#4b7bec")
ax1.plot(monthly.month_dt, monthly.revenue / 1e6, color="#4b7bec", lw=2, label="Revenue ($M)")
ax2 = ax1.twinx()
ax2.plot(monthly.month_dt, monthly.profit / 1e6, color="#e94560", lw=2, ls="--", label="Profit ($M)")
ax1.set_xlabel("Month"); ax1.set_ylabel("Revenue ($M)", color="#4b7bec")
ax2.set_ylabel("Profit ($M)", color="#e94560")
ax1.set_title("Monthly Revenue & Profit Trend (2022-2024)")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("../python/charts/01_monthly_trend.png")
plt.close()
log.info("Chart 1 saved: monthly trend")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 2 – Revenue by Region (Bar)
# ═══════════════════════════════════════════════════════════════════════════════
reg = completed.groupby("region").agg(revenue=("net_revenue","sum"),
                                       profit=("profit","sum")).sort_values("revenue", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(reg.index, reg.revenue / 1e6, color=COLORS[:len(reg)], width=0.6, edgecolor="white", lw=1.2)
ax.bar(reg.index, reg.profit / 1e6, color=[c + "88" for c in COLORS[:len(reg)]], width=0.6)
for bar, val in zip(bars, reg.revenue / 1e6):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"${val:.1f}M", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.set_title("Revenue & Profit by Region")
ax.set_ylabel("Amount ($M)")
ax.legend(["Revenue", "Profit"])
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("../python/charts/02_revenue_by_region.png")
plt.close()
log.info("Chart 2 saved: revenue by region")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 3 – Category Revenue Donut
# ═══════════════════════════════════════════════════════════════════════════════
cat = completed.groupby("category")["net_revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    cat.values, labels=cat.index, autopct="%1.1f%%",
    colors=COLORS[:len(cat)], startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(10); at.set_fontweight("bold")
ax.set_title("Revenue Share by Category")
plt.tight_layout()
plt.savefig("../python/charts/03_category_donut.png")
plt.close()
log.info("Chart 3 saved: category donut")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 4 – Sales Rep Performance (Horizontal Bar)
# ═══════════════════════════════════════════════════════════════════════════════
rep = completed.groupby("sales_rep").agg(
    revenue=("net_revenue","sum"),
    profit=("profit","sum"),
    orders=("order_id","count")
).sort_values("revenue")

fig, ax = plt.subplots(figsize=(10, 6))
y = range(len(rep))
ax.barh(list(y), rep.revenue / 1e6, color="#4b7bec", alpha=0.8, height=0.5, label="Revenue")
ax.barh(list(y), rep.profit / 1e6, color="#20bf6b", alpha=0.8, height=0.3, label="Profit")
ax.set_yticks(list(y)); ax.set_yticklabels(rep.index)
ax.set_xlabel("Amount ($M)"); ax.set_title("Sales Rep Performance")
ax.legend()
for i, (rev, prof) in enumerate(zip(rep.revenue / 1e6, rep.profit / 1e6)):
    ax.text(rev + 0.1, i, f"${rev:.1f}M", va="center", fontsize=8)
plt.tight_layout()
plt.savefig("../python/charts/04_sales_rep_performance.png")
plt.close()
log.info("Chart 4 saved: sales rep performance")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 5 – Profit Margin Distribution (Box)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
data_by_cat = [completed[completed.category==c]["profit_margin"].values * 100
               for c in completed.category.unique()]
bp = ax.boxplot(data_by_cat, labels=completed.category.unique(),
                patch_artist=True, notch=True)
for patch, color in zip(bp["boxes"], COLORS):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax.set_title("Profit Margin Distribution by Category")
ax.set_ylabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig("../python/charts/05_margin_distribution.png")
plt.close()
log.info("Chart 5 saved: margin distribution")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 6 – Quarterly Revenue Growth (Grouped Bar)
# ═══════════════════════════════════════════════════════════════════════════════
completed2 = completed.copy()
completed2["year"] = completed2.order_date.dt.year
completed2["quarter"] = completed2.order_date.dt.quarter
qtr = completed2.groupby(["year","quarter"])["net_revenue"].sum().reset_index()
qtr_pivot = qtr.pivot(index="quarter", columns="year", values="net_revenue") / 1e6

x = np.arange(4)
width = 0.25
fig, ax = plt.subplots(figsize=(10, 5))
for i, yr in enumerate(qtr_pivot.columns):
    bars = ax.bar(x + i*width, qtr_pivot[yr], width=width,
                  label=str(yr), color=COLORS[i+2], edgecolor="white")
ax.set_xticks(x + width)
ax.set_xticklabels([f"Q{q}" for q in range(1, 5)])
ax.set_xlabel("Quarter"); ax.set_ylabel("Revenue ($M)")
ax.set_title("Quarterly Revenue by Year"); ax.legend()
plt.tight_layout()
plt.savefig("../python/charts/06_quarterly_growth.png")
plt.close()
log.info("Chart 6 saved: quarterly growth")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 7 – Channel vs Category Heatmap
# ═══════════════════════════════════════════════════════════════════════════════
heat = completed.groupby(["channel","category"])["net_revenue"].sum().unstack(fill_value=0) / 1e6
fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(heat, annot=True, fmt=".1f", cmap="YlOrRd",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Revenue ($M)"})
ax.set_title("Revenue Heatmap: Channel × Category ($M)")
plt.tight_layout()
plt.savefig("../python/charts/07_channel_category_heatmap.png")
plt.close()
log.info("Chart 7 saved: channel×category heatmap")

# ═══════════════════════════════════════════════════════════════════════════════
# Chart 8 – Order Status Funnel
# ═══════════════════════════════════════════════════════════════════════════════
status_counts = df.status.value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(status_counts.index, status_counts.values,
              color=["#20bf6b","#f7b731","#e94560","#fc5c65"][:len(status_counts)],
              edgecolor="white", width=0.5)
for bar, val in zip(bars, status_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
            str(val), ha="center", fontweight="bold")
ax.set_title("Order Status Distribution")
ax.set_ylabel("Count")
plt.tight_layout()
plt.savefig("../python/charts/08_order_status.png")
plt.close()
log.info("Chart 8 saved: order status")

log.info("All 8 charts generated in ../python/charts/")

# ── Print EDA Summary ─────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EDA SUMMARY")
print("="*60)
print(f"Total Records      : {len(df):,}")
print(f"Completed Orders   : {len(completed):,}")
print(f"Date Range         : {df.order_date.min().date()} → {df.order_date.max().date()}")
print(f"Total Revenue      : ${completed.net_revenue.sum():,.0f}")
print(f"Total Profit       : ${completed.profit.sum():,.0f}")
print(f"Overall Margin     : {completed.profit_margin.mean()*100:.1f}%")
print(f"Avg Order Value    : ${completed.net_revenue.mean():,.0f}")
print(f"Top Region         : {completed.groupby('region')['net_revenue'].sum().idxmax()}")
print(f"Top Category       : {completed.groupby('category')['net_revenue'].sum().idxmax()}")
print(f"Top Sales Rep      : {completed.groupby('sales_rep')['net_revenue'].sum().idxmax()}")
print(f"Charts saved to    : ../python/charts/")
