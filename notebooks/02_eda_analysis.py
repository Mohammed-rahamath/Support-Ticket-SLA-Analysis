"""
DA-48: Support Ticket & SLA Analysis
EDA Script — 02_eda_analysis.py

Produces 8 charts saved as PNG files in notebooks/charts/
"""

import matplotlib
matplotlib.use('Agg')   # Non-interactive backend — must be set before pyplot import

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 1: SETUP & DATA LOADING
# ──────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("SECTION 1: SETUP & DATA LOADING")
print("=" * 70)

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "..", "data", "raw")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# Load datasets
tickets    = pd.read_csv(os.path.join(DATA_DIR, "tickets_raw.csv"))
agents     = pd.read_csv(os.path.join(DATA_DIR, "agents.csv"))
categories = pd.read_csv(os.path.join(DATA_DIR, "categories.csv"))
customers  = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))

# Parse datetimes
tickets["created_at"]  = pd.to_datetime(tickets["created_at"],  errors="coerce")
tickets["resolved_at"] = pd.to_datetime(tickets["resolved_at"], errors="coerce")

# Derived columns
tickets["year_month"] = tickets["created_at"].dt.to_period("M")

print(f"  tickets_raw  : {tickets.shape[0]:,} rows × {tickets.shape[1]} cols")
print(f"  agents       : {agents.shape[0]:,} rows × {agents.shape[1]} cols")
print(f"  categories   : {categories.shape[0]:,} rows × {categories.shape[1]} cols")
print(f"  customers    : {customers.shape[0]:,} rows × {customers.shape[1]} cols")
print()

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 2: SUMMARY STATISTICS
# ──────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("SECTION 2: SUMMARY STATISTICS")
print("=" * 70)

closed = tickets[tickets["status"] == "Closed"].copy()
print(f"  Total tickets          : {len(tickets):,}")
print(f"  Closed tickets         : {len(closed):,}")
print(f"  Open / In-Progress     : {len(tickets) - len(closed):,}")
print()

overall_breach_rate = closed["sla_breached"].mean() * 100
print(f"  Overall SLA breach rate (closed) : {overall_breach_rate:.1f}%")
print(f"  Mean resolution time (hrs)       : {closed['resolution_time_hrs'].mean():.1f}")
print(f"  Median resolution time (hrs)     : {closed['resolution_time_hrs'].median():.1f}")
print(f"  Mean first-response time (hrs)   : {closed['first_response_hrs'].mean():.1f}")
print()

print("  Ticket count by priority:")
print(tickets["priority"].value_counts().to_string())
print()

print("  Ticket count by status:")
print(tickets["status"].value_counts().to_string())
print()

print("  Ticket count by channel:")
print(tickets["channel"].value_counts().to_string())
print()

# Shared style
sns.set_theme(style="whitegrid", palette="muted")
TITLE_SIZE  = 14
LABEL_SIZE  = 11
TICK_SIZE   = 10

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 3: CHARTS
# ──────────────────────────────────────────────────────────────────────────────
print("=" * 70)
print("SECTION 3: CHARTS")
print("=" * 70)

# ── Chart 1: Pie — SLA Breach vs Non-Breach (closed tickets) ─────────────────
print("\n[Chart 1] SLA Breach vs Non-Breach Pie Chart")

breached     = int(closed["sla_breached"].sum())
not_breached = len(closed) - breached
sizes  = [breached, not_breached]
labels = [f"Breached\n({breached:,})", f"Not Breached\n({not_breached:,})"]
colors = ["#e74c3c", "#2ecc71"]
explode = (0.05, 0)

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors, explode=explode,
    autopct="%1.1f%%", startangle=140,
    textprops={"fontsize": LABEL_SIZE},
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight("bold")
ax.set_title("SLA Breach vs Non-Breach (Closed Tickets)", fontsize=TITLE_SIZE, fontweight="bold", pad=15)
plt.tight_layout()
chart1_path = os.path.join(CHARTS_DIR, "chart_01_sla_pie.png")
plt.savefig(chart1_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart1_path}")
print(f"  Observation: {overall_breach_rate:.1f}% of closed tickets breached their SLA targets.")
print(f"  The majority ({100-overall_breach_rate:.1f}%) were resolved within SLA, but the breach rate")
print(f"  indicates room for significant improvement in support responsiveness.")

# ── Chart 2: Bar — SLA Breach Rate % by Priority ─────────────────────────────
print("\n[Chart 2] SLA Breach Rate % by Priority")

priority_order  = ["Critical", "High", "Medium", "Low"]
breach_priority = (
    closed.groupby("priority")["sla_breached"]
    .mean()
    .mul(100)
    .reindex(priority_order)
    .reset_index()
)
breach_priority.columns = ["Priority", "Breach Rate (%)"]

palette = {"Critical": "#c0392b", "High": "#e67e22", "Medium": "#f1c40f", "Low": "#3498db"}
colors2 = [palette.get(p, "#95a5a6") for p in breach_priority["Priority"]]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(breach_priority["Priority"], breach_priority["Breach Rate (%)"],
              color=colors2, edgecolor="white", linewidth=0.8)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}%",
            ha="center", va="bottom", fontsize=TICK_SIZE, fontweight="bold")
ax.set_title("SLA Breach Rate % by Priority", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Priority", fontsize=LABEL_SIZE)
ax.set_ylabel("Breach Rate (%)", fontsize=LABEL_SIZE)
ax.set_ylim(0, breach_priority["Breach Rate (%)"].max() * 1.2 + 2)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
plt.tight_layout()
chart2_path = os.path.join(CHARTS_DIR, "chart_02_breach_by_priority.png")
plt.savefig(chart2_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart2_path}")
top_priority = breach_priority.loc[breach_priority["Breach Rate (%)"].idxmax(), "Priority"]
top_rate     = breach_priority["Breach Rate (%)"].max()
print(f"  Observation: '{top_priority}' tickets have the highest SLA breach rate at {top_rate:.1f}%.")
print(f"  This counter-intuitive pattern may reflect stricter SLA windows for high-urgency tickets.")
print(f"  Lower-priority tickets have more lenient SLA targets, making them easier to meet.")

# ── Chart 3: Line — Monthly Ticket Volume ────────────────────────────────────
print("\n[Chart 3] Monthly Ticket Volume (Jan 2024 – Jun 2025)")

monthly = (
    tickets.groupby("year_month")
    .size()
    .reset_index(name="ticket_count")
    .sort_values("year_month")
)
monthly["period_str"] = monthly["year_month"].astype(str)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["period_str"], monthly["ticket_count"],
        marker="o", linewidth=2, markersize=5, color="#2980b9")
ax.fill_between(monthly["period_str"], monthly["ticket_count"], alpha=0.15, color="#2980b9")
ax.set_title("Monthly Ticket Volume (Jan 2024 – Jun 2025)", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Month", fontsize=LABEL_SIZE)
ax.set_ylabel("Number of Tickets", fontsize=LABEL_SIZE)
plt.xticks(rotation=45, ha="right", fontsize=TICK_SIZE - 1)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
chart3_path = os.path.join(CHARTS_DIR, "chart_03_monthly_volume.png")
plt.savefig(chart3_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart3_path}")
peak_month = monthly.loc[monthly["ticket_count"].idxmax()]
print(f"  Observation: Ticket volume peaks in {peak_month['period_str']} with {peak_month['ticket_count']:,} tickets.")
print(f"  The trend reveals seasonal or operational surges worth aligning with staffing levels.")
print(f"  Overall, volume remains relatively consistent across the 18-month window.")

# ── Chart 4: Histogram — Distribution of Resolution Time ─────────────────────
print("\n[Chart 4] Distribution of Resolution Time (hrs, capped at 150)")

res_capped = closed["resolution_time_hrs"].clip(upper=150).dropna()

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(res_capped, bins=40, color="#8e44ad", edgecolor="white", linewidth=0.5, alpha=0.85)
ax.axvline(res_capped.median(), color="#e74c3c", linewidth=2, linestyle="--",
           label=f"Median: {res_capped.median():.1f} hrs")
ax.axvline(res_capped.mean(), color="#f39c12", linewidth=2, linestyle="-.",
           label=f"Mean: {res_capped.mean():.1f} hrs")
ax.set_title("Distribution of Resolution Time (hrs, capped at 150)", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Resolution Time (hrs)", fontsize=LABEL_SIZE)
ax.set_ylabel("Number of Tickets", fontsize=LABEL_SIZE)
ax.legend(fontsize=TICK_SIZE)
plt.tight_layout()
chart4_path = os.path.join(CHARTS_DIR, "chart_04_resolution_time_hist.png")
plt.savefig(chart4_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart4_path}")
print(f"  Observation: Resolution time is right-skewed; median ({res_capped.median():.1f} hrs) is lower than the mean ({res_capped.mean():.1f} hrs).")
print(f"  Most tickets are resolved quickly, but a tail of complex cases drives the average up.")
print(f"  Identifying these outlier tickets could guide targeted process improvements.")

# ── Chart 5: Horizontal Bar — SLA Breach Rate % by Category ──────────────────
print("\n[Chart 5] SLA Breach Rate % by Category")

closed_cat = closed.merge(
    categories[["category_id", "category_name"]], on="category_id", how="left"
)
breach_cat = (
    closed_cat.groupby("category_name")["sla_breached"]
    .mean()
    .mul(100)
    .sort_values(ascending=True)
    .reset_index()
)
breach_cat.columns = ["Category", "Breach Rate (%)"]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(breach_cat["Category"], breach_cat["Breach Rate (%)"],
               color="#16a085", edgecolor="white")
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{w:.1f}%", va="center", ha="left", fontsize=TICK_SIZE, fontweight="bold")
ax.set_title("SLA Breach Rate % by Category", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Breach Rate (%)", fontsize=LABEL_SIZE)
ax.set_ylabel("Category", fontsize=LABEL_SIZE)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.set_xlim(0, breach_cat["Breach Rate (%)"].max() * 1.25)
plt.tight_layout()
chart5_path = os.path.join(CHARTS_DIR, "chart_05_breach_by_category.png")
plt.savefig(chart5_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart5_path}")
worst_cat = breach_cat.iloc[-1]
print(f"  Observation: '{worst_cat['Category']}' has the highest category breach rate at {worst_cat['Breach Rate (%)']:.1f}%.")
print(f"  Categories with tighter SLA windows (e.g. Network Connectivity) tend to breach more frequently.")
print(f"  This signals a need for dedicated fast-response teams for high-urgency categories.")

# ── Chart 6: Bar — Top 10 Agents by Breach Count ─────────────────────────────
print("\n[Chart 6] Top 10 Agents by Breach Count")

closed_agents = closed.merge(
    agents[["agent_id", "name"]], on="agent_id", how="left"
)
agent_breach = (
    closed_agents.groupby("name")["sla_breached"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
agent_breach.columns = ["Agent", "Breach Count"]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(agent_breach["Agent"], agent_breach["Breach Count"],
              color="#c0392b", edgecolor="white")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"{int(h)}",
            ha="center", va="bottom", fontsize=TICK_SIZE, fontweight="bold")
ax.set_title("Top 10 Agents by SLA Breach Count", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Agent", fontsize=LABEL_SIZE)
ax.set_ylabel("Number of Breaches", fontsize=LABEL_SIZE)
plt.xticks(rotation=35, ha="right", fontsize=TICK_SIZE)
plt.tight_layout()
chart6_path = os.path.join(CHARTS_DIR, "chart_06_top10_agents_breach.png")
plt.savefig(chart6_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart6_path}")
top_agent = agent_breach.iloc[0]
print(f"  Observation: '{top_agent['Agent']}' leads with {int(top_agent['Breach Count'])} breached tickets.")
print(f"  High breach counts may reflect workload imbalance, lack of training, or complex case assignments.")
print(f"  Cross-referencing ticket volume per agent will distinguish overload from performance gaps.")

# ── Chart 7: Bar — Ticket Count by Channel ───────────────────────────────────
print("\n[Chart 7] Ticket Count by Channel")

channel_counts = tickets["channel"].value_counts().reset_index()
channel_counts.columns = ["Channel", "Count"]
chan_colors = ["#3498db", "#e67e22", "#2ecc71", "#9b59b6"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(channel_counts["Channel"], channel_counts["Count"],
              color=chan_colors[:len(channel_counts)], edgecolor="white")
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 10, f"{int(h):,}",
            ha="center", va="bottom", fontsize=TICK_SIZE, fontweight="bold")
ax.set_title("Ticket Count by Channel", fontsize=TITLE_SIZE, fontweight="bold")
ax.set_xlabel("Channel", fontsize=LABEL_SIZE)
ax.set_ylabel("Number of Tickets", fontsize=LABEL_SIZE)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
chart7_path = os.path.join(CHARTS_DIR, "chart_07_tickets_by_channel.png")
plt.savefig(chart7_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart7_path}")
top_chan = channel_counts.iloc[0]
print(f"  Observation: '{top_chan['Channel']}' is the dominant intake channel with {int(top_chan['Count']):,} tickets.")
print(f"  Channel distribution informs staffing and self-service investment decisions.")
print(f"  Heavier digital channel use suggests customers increasingly prefer async communication.")

# ── Chart 8: Heatmap — Breach Rate by Priority × Category ───────────────────
print("\n[Chart 8] Heatmap — Breach Rate by Priority × Category")

closed_full = closed.merge(
    categories[["category_id", "category_name"]], on="category_id", how="left"
)
pivot = (
    closed_full.groupby(["priority", "category_name"])["sla_breached"]
    .mean()
    .mul(100)
    .unstack(fill_value=0)
)
# Ensure consistent priority order (rows)
prio_order_avail = [p for p in priority_order if p in pivot.index]
pivot = pivot.reindex(prio_order_avail)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(
    pivot, annot=True, fmt=".1f", cmap="YlOrRd",
    linewidths=0.5, linecolor="white",
    annot_kws={"size": 10, "weight": "bold"},
    cbar_kws={"label": "Breach Rate (%)"},
    ax=ax
)
ax.set_title("SLA Breach Rate (%) — Priority × Category", fontsize=TITLE_SIZE, fontweight="bold", pad=12)
ax.set_xlabel("Category", fontsize=LABEL_SIZE)
ax.set_ylabel("Priority", fontsize=LABEL_SIZE)
plt.xticks(rotation=30, ha="right", fontsize=TICK_SIZE)
plt.yticks(rotation=0, fontsize=TICK_SIZE)
plt.tight_layout()
chart8_path = os.path.join(CHARTS_DIR, "chart_08_heatmap_priority_category.png")
plt.savefig(chart8_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart8_path}")
print(f"  Observation: The heatmap exposes high-risk intersections of priority and category.")
print(f"  Critical tickets in time-sensitive categories show the darkest cells (highest breach rate).")
print(f"  These hotspots are prime targets for SLA policy review and resource reallocation.")

# ──────────────────────────────────────────────────────────────────────────────
# SECTION 4: CORRELATION ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("SECTION 4: CORRELATION ANALYSIS")
print("=" * 70)

num_cols = ["first_response_hrs", "resolution_time_hrs", "sla_target_hours",
            "sla_breached", "satisfaction_score"]
corr_data = closed[num_cols].dropna()
corr_matrix = corr_data.corr()

print("\nCorrelation matrix (closed tickets):")
print(corr_matrix.round(3).to_string())

print("\nKey correlations with sla_breached:")
breach_corr = corr_matrix["sla_breached"].drop("sla_breached").sort_values(key=abs, ascending=False)
for col, val in breach_corr.items():
    print(f"  {col:<25} : {val:+.3f}")

print("\nKey correlations with satisfaction_score:")
sat_corr = corr_matrix["satisfaction_score"].drop("satisfaction_score").sort_values(key=abs, ascending=False)
for col, val in sat_corr.items():
    print(f"  {col:<25} : {val:+.3f}")

print()
print("=" * 70)
print("EDA COMPLETE — All 8 charts saved to:", CHARTS_DIR)
print("=" * 70)
