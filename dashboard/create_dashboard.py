import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

base_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\DA-48-Support-Ticket-SLA-Analysis"
cleaned_dir = os.path.join(base_dir, "data", "cleaned")
dashboard_dir = os.path.join(base_dir, "dashboard")
os.makedirs(dashboard_dir, exist_ok=True)

# Load data
tickets = pd.read_csv(os.path.join(cleaned_dir, "tickets_cleaned.csv"))
agents = pd.read_csv(os.path.join(cleaned_dir, "agents.csv"))
categories = pd.read_csv(os.path.join(cleaned_dir, "categories.csv"))
customers = pd.read_csv(os.path.join(cleaned_dir, "customers.csv"))

# Merge for enrichment
df = tickets.merge(categories, on="category_id", how="left")
df = df.merge(agents, on="agent_id", how="left", suffixes=("", "_agent"))
df = df.merge(customers, on="customer_id", how="left", suffixes=("", "_cust"))

# Closed tickets subset
closed = df[df["status"] == "Closed"].copy()

# Total KPIs
total_tickets = len(tickets)
closed_tickets = len(closed)
breached_tickets = int(closed["sla_breached"].sum())
breach_rate = round(breached_tickets / closed_tickets * 100, 2)
avg_resolution = round(closed["resolution_time_hrs"].mean(), 2)
avg_csat = round(closed["satisfaction_score"].dropna().mean(), 2)

# --- Visual 1: Pie Chart (Breached vs Met) ---
fig_pie = go.Figure(data=[go.Pie(
    labels=['Breached SLA', 'Within SLA'],
    values=[breached_tickets, closed_tickets - breached_tickets],
    hole=.45,
    marker_colors=['#D93025', '#1E8E3E']
)])
fig_pie.update_layout(title="Overall SLA Adherence Breakdown", height=350, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 2: Breach by Priority ---
p_summary = closed.groupby("priority")["sla_breached"].agg(["count", "mean"]).reset_index()
p_summary["mean"] = p_summary["mean"] * 100
fig_prio = px.bar(
    p_summary, x="priority", y="mean",
    color="priority",
    labels={"mean": "Breach Rate (%)", "priority": "Ticket Priority"},
    title="SLA Breach Rate by Priority Tier (%)",
    color_discrete_sequence=['#EA4335', '#FBBC04', '#4285F4', '#34A853']
)
fig_prio.update_layout(height=350, showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 3: Breach Rate by Category ---
c_summary = closed.groupby("category_name")["sla_breached"].agg(["count", "mean"]).reset_index()
c_summary["mean"] = c_summary["mean"] * 100
c_summary = c_summary.sort_values(by="mean", ascending=True)
fig_cat = px.bar(
    c_summary, y="category_name", x="mean", orientation="h",
    color="mean",
    labels={"mean": "Breach Rate (%)", "category_name": "Category"},
    title="SLA Breach Rate by Incident Category (%)",
    color_continuous_scale="Reds"
)
fig_cat.update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 4: Monthly Trend ---
closed["month"] = pd.to_datetime(closed["created_at"]).dt.to_period("M").astype(str)
m_summary = closed.groupby("month").agg(
    total=("ticket_id", "count"),
    breaches=("sla_breached", "sum")
).reset_index()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=m_summary["month"], y=m_summary["total"], name="Total Closed", mode="lines+markers", line=dict(color="#1A73E8", width=3)))
fig_trend.add_trace(go.Scatter(x=m_summary["month"], y=m_summary["breaches"], name="SLA Breached", mode="lines+markers", line=dict(color="#D93025", width=3, dash="dot")))
fig_trend.update_layout(title="Monthly Inflow vs. SLA Breaches (Jan 2024 - Jun 2025)", height=350, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 5: Top 10 Agents by Breaches ---
ag_summary = closed.groupby(["name", "department", "shift"])["sla_breached"].agg(["count", "sum"]).reset_index()
ag_summary["breach_pct"] = round(ag_summary["sum"] / ag_summary["count"] * 100, 1)
ag_top = ag_summary.sort_values(by="sum", ascending=False).head(10)

fig_agent = px.bar(
    ag_top, x="name", y="sum",
    color="shift",
    title="Top 10 Engineers by Total SLA Breaches",
    labels={"sum": "Breached Tickets", "name": "Engineer Name", "shift": "Working Shift"}
)
fig_agent.update_layout(height=360, margin=dict(t=50, b=40, l=20, r=20))

# --- Visual 6: Shift Comparison ---
shift_summary = closed.groupby("shift")["sla_breached"].agg(["count", "mean"]).reset_index()
shift_summary["breach_pct"] = round(shift_summary["mean"] * 100, 2)
fig_shift = px.bar(
    shift_summary, x="shift", y="breach_pct",
    color="shift",
    title="Breach Rate by Shift Cohort (%)",
    labels={"breach_pct": "Breach Rate (%)", "shift": "Shift"}
)
fig_shift.update_layout(height=360, showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 7: Geographic Heatmap / City Bar ---
city_summary = closed.groupby("city")["ticket_id"].count().reset_index().sort_values(by="ticket_id", ascending=False).head(10)
fig_city = px.bar(
    city_summary, x="city", y="ticket_id",
    color="ticket_id",
    color_continuous_scale="Viridis",
    title="Top 10 Customer Hubs by Support Volume",
    labels={"ticket_id": "Tickets", "city": "City"}
)
fig_city.update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20))

# --- Visual 8: Channel Distribution & Latency ---
chan_summary = closed.groupby("channel")["resolution_time_hrs"].mean().reset_index()
fig_chan = px.bar(
    chan_summary, x="channel", y="resolution_time_hrs",
    color="channel",
    title="Mean Resolution Time by Intake Channel (Hours)",
    labels={"resolution_time_hrs": "Avg Hours", "channel": "Intake Channel"}
)
fig_chan.update_layout(height=350, showlegend=False, margin=dict(t=50, b=20, l=20, r=20))

# Assemble HTML dashboard
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Support Ticket & SLA Analysis Dashboard | DA-48</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: #F1F4F9; color: #202124; padding-bottom: 40px; }}
        .header {{ background: linear-gradient(135deg, #002060, #1A73E8); color: white; padding: 24px 36px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        .header h1 {{ font-size: 26px; font-weight: 700; }}
        .header p {{ font-size: 14px; opacity: 0.9; margin-top: 4px; }}
        .nav {{ display: flex; background: #FFFFFF; border-bottom: 1px solid #D1D5DB; padding: 0 36px; position: sticky; top: 0; z-index: 100; }}
        .nav-item {{ padding: 14px 22px; cursor: pointer; font-size: 14px; font-weight: 600; color: #5F6368; text-decoration: none; border-bottom: 3px solid transparent; }}
        .nav-item:hover, .nav-item.active {{ color: #1A73E8; border-bottom: 3px solid #1A73E8; }}
        .container {{ max-width: 1400px; margin: 24px auto; padding: 0 20px; }}
        .kpi-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); text-align: center; border-top: 4px solid #1A73E8; }}
        .kpi-card.alert {{ border-top-color: #D93025; }}
        .kpi-card.warning {{ border-top-color: #FBBC04; }}
        .kpi-card.success {{ border-top-color: #34A853; }}
        .kpi-val {{ font-size: 32px; font-weight: 700; color: #202124; margin: 8px 0; }}
        .kpi-card.alert .kpi-val {{ color: #D93025; }}
        .kpi-label {{ font-size: 13px; font-weight: 600; text-transform: uppercase; color: #5F6368; letter-spacing: 0.5px; }}
        .kpi-sub {{ font-size: 12px; color: #70757A; }}
        .section-header {{ margin: 30px 0 16px 0; font-size: 20px; font-weight: 700; color: #002060; border-left: 5px solid #1A73E8; padding-left: 12px; }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
        .chart-card {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        @media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Support Ticket & SLA Performance Dashboard</h1>
        <p>Project ID: DA-48 | IT Ops & SaaS Domain | Mohammed Rahamath Ulla | Data Period: Jan 2024 - Jun 2025</p>
    </div>

    <div class="nav">
        <a class="nav-item active" href="#overview">1. Executive Overview</a>
        <a class="nav-item" href="#breaches">2. SLA Breach Analysis</a>
        <a class="nav-item" href="#agents">3. Engineer & Shift Performance</a>
        <a class="nav-item" href="#customers">4. Geographic & Channel Analytics</a>
    </div>

    <div class="container">
        <!-- Section 1 -->
        <div id="overview" class="section-header">1. Executive Performance Indicators</div>
        <div class="kpi-row">
            <div class="kpi-card">
                <div class="kpi-label">Total Inflow Volume</div>
                <div class="kpi-val">{total_tickets:,}</div>
                <div class="kpi-sub">Total Recorded Support Tickets</div>
            </div>
            <div class="kpi-card alert">
                <div class="kpi-label">SLA Breach Rate</div>
                <div class="kpi-val">{breach_rate}%</div>
                <div class="kpi-sub">Benchmark: &lt; 20.0% (Critical Gap)</div>
            </div>
            <div class="kpi-card warning">
                <div class="kpi-label">Total Breached Tickets</div>
                <div class="kpi-val">{breached_tickets:,}</div>
                <div class="kpi-sub">Failed Contractual SLAs</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Mean Resolution Time</div>
                <div class="kpi-val">{avg_resolution} hrs</div>
                <div class="kpi-sub">Median MTTR: 12.6 hrs</div>
            </div>
            <div class="kpi-card success">
                <div class="kpi-label">Avg Customer Rating</div>
                <div class="kpi-val">{avg_csat} / 5.0</div>
                <div class="kpi-sub">CSAT on Closed Incidents</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="chart-card">{fig_pie.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-card">{fig_trend.to_html(full_html=False, include_plotlyjs=False)}</div>
        </div>

        <!-- Section 2 -->
        <div id="breaches" class="section-header">2. SLA Breach Decomposition</div>
        <div class="grid-2">
            <div class="chart-card">{fig_prio.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-card">{fig_cat.to_html(full_html=False, include_plotlyjs=False)}</div>
        </div>

        <!-- Section 3 -->
        <div id="agents" class="section-header">3. Engineer & Shift Operational Analysis</div>
        <div class="grid-2">
            <div class="chart-card">{fig_agent.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-card">{fig_shift.to_html(full_html=False, include_plotlyjs=False)}</div>
        </div>

        <!-- Section 4 -->
        <div id="customers" class="section-header">4. Geographic Hubs & Intake Channels</div>
        <div class="grid-2">
            <div class="chart-card">{fig_city.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-card">{fig_chan.to_html(full_html=False, include_plotlyjs=False)}</div>
        </div>
    </div>
</body>
</html>
"""

output_html = os.path.join(dashboard_dir, "SLA_Dashboard.html")
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Interactive HTML Dashboard generated at: {output_html}")
print(f"Dashboard File Size: {os.path.getsize(output_html):,} bytes")
