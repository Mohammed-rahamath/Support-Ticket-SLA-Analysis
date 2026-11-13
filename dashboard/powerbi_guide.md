# Deliverable 5: Power BI Dashboard — Step-by-Step Build Guide
**Project DA-48 | Support Ticket & SLA Analysis**

---

## Setup

1. Open **Power BI Desktop**
2. Click **Get Data → Text/CSV**
3. Load all 4 cleaned files from `data/cleaned/`:
   - `tickets_cleaned.csv`
   - `agents.csv`
   - `categories.csv`
   - `customers.csv`

## Create Relationships (Model View)

Go to **Model View** and set:
| From Table | Column | To Table | Column | Cardinality |
|------------|--------|----------|--------|-------------|
| tickets | category_id | categories | category_id | Many → One |
| tickets | agent_id | agents | agent_id | Many → One |
| tickets | customer_id | customers | customer_id | Many → One |

## DAX Measures (Create in Report View → New Measure)

```dax
Total Tickets = COUNTROWS(tickets_cleaned)

Closed Tickets = CALCULATE(COUNTROWS(tickets_cleaned), tickets_cleaned[status] = "Closed")

SLA Breached Count = CALCULATE(COUNTROWS(tickets_cleaned), tickets_cleaned[sla_breached] = 1)

SLA Breach Rate % = DIVIDE([SLA Breached Count], [Closed Tickets], 0) * 100

Avg Resolution Hrs = AVERAGE(tickets_cleaned[resolution_time_hrs])

Avg Satisfaction = AVERAGE(tickets_cleaned[satisfaction_score])
```

---

## Page 1: 📊 Executive Overview

| Visual | Type | Fields |
|--------|------|--------|
| Total Tickets | KPI Card | Measure: Total Tickets |
| SLA Breach Rate | KPI Card | Measure: SLA Breach Rate % |
| Avg Resolution Time | KPI Card | Measure: Avg Resolution Hrs |
| Avg Satisfaction | KPI Card | Measure: Avg Satisfaction |
| Ticket Status Split | Donut Chart | Legend: status, Values: Count |
| Breach vs Non-Breach | Pie Chart | Legend: sla_breached, Values: Count |

**Slicers to add:**
- Date Range slicer on `created_at`
- Priority slicer (Critical/High/Medium/Low)

---

## Page 2: 🔴 SLA Breach Analysis

| Visual | Type | Fields |
|--------|------|--------|
| Breach Rate by Priority | Clustered Bar | X-axis: priority, Y-axis: SLA Breach Rate % |
| Breach Rate by Category | Horizontal Bar | Y-axis: category_name (categories), X-axis: SLA Breach Rate % |
| Monthly Breach Trend | Line Chart | X-axis: created_at (Month), Y-axis: SLA Breached Count |
| Breach by Channel | Bar Chart | X-axis: channel, Y-axis: SLA Breach Rate % |

**Slicers:** Category, Status, Date Range

---

## Page 3: 👤 Agent Performance

| Visual | Type | Fields |
|--------|------|--------|
| Top 10 Agents by Breaches | Bar Chart (Top N filter = 10) | X: name (agents), Y: SLA Breached Count |
| Dept Breach Comparison | Clustered Bar | X: department (agents), Y: SLA Breach Rate % |
| Agent Table | Table Visual | name, department, shift, Total Tickets, SLA Breached Count, Avg Resolution Hrs |
| Breach by Shift | Bar Chart | X: shift, Y: SLA Breach Rate % |

---

## Page 4: 🗺️ Customer & Geography

| Visual | Type | Fields |
|--------|------|--------|
| Tickets by City | Bar Chart (Top 10) | X: city (customers), Y: Total Tickets |
| Satisfaction by City | Bar Chart | X: city, Y: Avg Satisfaction |
| Satisfaction vs Breach (scatter) | Scatter Chart | X: Avg Resolution Hrs, Y: Avg Satisfaction |

---

## Formatting Tips

- Use **red** for breached values, **green** for within-SLA
- Set dashboard theme to a clean **corporate blue** theme
- Add a **title text box** on each page (e.g., "Executive Overview — DA-48 SLA Analysis")
- Enable **cross-filtering** so clicking one visual filters all others on the page
- Export each page as PDF via **File → Export → PDF** for submission backup
