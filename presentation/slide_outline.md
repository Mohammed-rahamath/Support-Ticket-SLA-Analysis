# Deliverable 7: Presentation Slide Deck Outline
**Project DA-48 | Support Ticket & SLA Analysis | 5-Minute Presentation**

---

## Slide 1 — Title Slide
**Title:** Support Ticket & SLA Analysis  
**Subtitle:** DA-48 | Data Analytics Project  
**Your Name:** Mohammed Rahamath Ulla  
**Date:** November 2026  
*(Add a relevant background image — e.g., helpdesk/IT operations)*

---

## Slide 2 — The Business Problem
**Heading:** Why Does SLA Matter?

**Content (3 bullet points):**
- An IT support company handles 5,000+ tickets/month across 5 categories
- SLA (Service Level Agreement) = maximum time to resolve each ticket
- **Breaching SLA** leads to: customer dissatisfaction, penalty clauses, lost contracts

**Visual:** Simple diagram showing: Ticket Created → SLA Window → Resolved (within/breached)

---

## Slide 3 — Dataset Overview
**Heading:** Data Used in This Project

**Content (table):**
| Table | Rows | Key Columns |
|-------|------|-------------|
| Tickets | 5,060 | ticket_id, priority, status, resolution_time_hrs, sla_breached |
| Agents | 150 | agent_id, name, department, shift |
| Categories | 5 | category_name, sla_target_hours |
| Customers | 1,000 | customer_id, city, state |

**Source:** Kaggle — Customer Support Ticket Dataset

---

## Slide 4 — Data Cleaning Summary
**Heading:** What We Fixed Before Analysis

**Content (icons + bullets):**
- 🔴 **102 null agent_id** values → filled with mode
- 🔁 **60 duplicate rows** → removed
- 🔡 **~150 inconsistent priority** values (lowercase) → standardized
- ⚡ **10 outlier resolution times** (>500 hrs) → removed
- ✅ Final cleaned dataset: **4,935 rows**

---

## Slide 5 — Key Finding 1: Overall Breach Rate
**Heading:** 53% of Tickets Breach SLA

**Visual:** Large donut chart (breach vs non-breach)

**Callout text:** Industry benchmark: < 20% | Our rate: 53% ⚠️

---

## Slide 6 — Key Finding 2: Breach by Priority & Category
**Heading:** Where Are Breaches Happening?

**Visuals (2 side-by-side bar charts):**
- Left: Breach rate by Priority (Critical highest)
- Right: Breach rate by Category (Network Connectivity highest — 4-hr SLA)

**Insight text:** Network Connectivity tickets average **5.6 hrs** vs **4-hr SLA target**

---

## Slide 7 — Key Finding 3: Agent & Shift Analysis
**Heading:** Who and When?

**Visual:** Top 5 agents by breach count (bar chart)

**Key insight:** Night shift agents have **2× higher** breach rate than Morning shift

---

## Slide 8 — Key Finding 4: Trend & Seasonality
**Heading:** Ticket Volumes Peak Mid-Year

**Visual:** Line chart — Monthly ticket volume Jan 2024–Jun 2025

**Insight:** May–June 2024 spike = highest breach period of the year

---

## Slide 9 — Power BI Dashboard Demo
**Heading:** Interactive Dashboard (Live Demo)

**Content:** Show the Power BI dashboard live
- Overview KPIs
- SLA Breach Analysis page
- Agent Performance page

*(If live demo not possible, add 2-3 screenshots of the dashboard)*

---

## Slide 10 — Recommendations
**Heading:** How to Fix This (Top 3 Recommendations)

| # | Recommendation | Expected Impact |
|---|---------------|----------------|
| 1 | 🔴 Dedicated Critical Response Team | -40% Network breaches |
| 2 | ⏰ Automated SLA Alert at 70% window | -25% preventable breaches |
| 3 | 🌙 Add 2 Night Shift Agents | -35% overnight breaches |

---

## Slide 11 — Conclusion
**Heading:** Summary

**Content:**
- Analyzed **5,060 tickets** across 18 months
- Found **53% SLA breach rate** — 2.6× above industry standard
- Root causes: understaffed critical team, night-shift gaps, peak-season spikes
- **3 targeted recommendations** can halve the breach rate within 2 quarters

**Thank you! | Questions?**

---

## Viva Prep: Expected Questions & Answers

**Q: Why did you choose this dataset?**  
A: SLA analysis is a core IT operations problem. The dataset had all 4 required tables and meaningful business context.

**Q: What was the most surprising finding?**  
A: Night-shift agents have 2× the breach rate of morning-shift agents, suggesting the problem is partly structural, not just individual.

**Q: How did you handle missing agent_id values?**  
A: I filled ~100 null agent_ids with the mode (most frequent agent_id) to preserve the row count and not bias the dataset by dropping them.

**Q: What does the window function in your SQL do?**  
A: Query 10 uses `SUM(sla_breached) OVER (ORDER BY month)` to compute a running total of monthly SLA breaches — useful for spotting cumulative trends.

**Q: How is sla_breached calculated?**  
A: `sla_breached = 1` if `resolution_time_hrs > sla_target_hours`, else `0`. This is derived for each closed ticket.
