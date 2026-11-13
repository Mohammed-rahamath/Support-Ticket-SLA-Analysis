# Deliverable 6: Insights & Recommendations Report
**Project DA-48 | Support Ticket & SLA Analysis**  
**Student:** Mohammed Rahamath Ulla  
**Date:** November 2026

---

## Executive Summary

This report analyses 5,060 IT support tickets raised between January 2024 and June 2025 to understand SLA breach patterns. The analysis combines SQL queries, Python EDA, and an interactive Power BI dashboard. Key findings reveal a 53% SLA breach rate among closed tickets, with Network Connectivity and Critical-priority tickets as the leading breach drivers.

---

## 1. Key Findings

### Finding 1 — High Overall SLA Breach Rate
- **53% of all closed tickets** breached their SLA target.
- This is significantly above the industry benchmark of < 20%, indicating a systemic issue in ticket resolution speed.

### Finding 2 — Critical & High Priority Tickets Breach Most
- **Critical-priority tickets** have the highest breach rate despite having a tighter 4-hour SLA (Network Connectivity).
- This suggests the team lacks dedicated fast-response capacity for critical issues.

### Finding 3 — Network Connectivity is the Top Breach Category
- With a strict **4-hour SLA**, Network Connectivity tickets are breached most frequently.
- Average resolution time for Network tickets is approximately **5.6 hours** — 40% over the SLA limit.

### Finding 4 — Seasonal Volume Spikes in Mid-Year
- Ticket volume peaked in **May–June 2024**, correlating with higher breach rates in that period.
- This suggests inadequate staffing planning for peak seasons.

### Finding 5 — Uneven Agent Performance
- The top 10 agents by breach count account for over **30% of all breaches** despite representing only 7% of agents.
- Some agents in Night shift have significantly higher breach rates, indicating shift-coverage gaps.

### Finding 6 — Low Customer Satisfaction Correlates with Breaches
- Closed tickets with SLA breaches received an average satisfaction score of **2.1 / 5**.
- Tickets resolved within SLA averaged **4.0 / 5** — nearly double.

### Finding 7 — Phone & Chat Channels Resolve Faster
- Tickets raised via **Phone and Chat** channels resolve 20% faster on average compared to Email tickets.
- Portal-raised tickets have the highest breach rate.

---

## 2. Business Impact

| Issue | Business Impact |
|-------|----------------|
| 53% SLA breach rate | Contract penalty risk; customer churn |
| Low satisfaction (2.1/5) on breached tickets | Negative reviews, lost renewals |
| Night shift coverage gaps | Overnight critical issues go unresolved |
| Portal ticket delays | Customers using self-service are least served |

---

## 3. Recommendations

### Recommendation 1 — Dedicated Critical Response Team 🔴
**Action:** Create a dedicated 3-agent rapid response team for Critical/High priority Network Connectivity tickets with a 2-hour internal target (buffer before 4-hour SLA).  
**Expected Impact:** Reduce Network Connectivity breach rate by ~40%.

### Recommendation 2 — SLA Alert System ⏰
**Action:** Implement automated alerts when a ticket reaches 70% of its SLA window without resolution. Notify both the assigned agent and their supervisor.  
**Expected Impact:** Agents can re-prioritize before breach occurs; estimated 25% reduction in preventable breaches.

### Recommendation 3 — Seasonal Staffing Plan 📅
**Action:** Hire 5–8 contract agents for May–July based on historical spike data. Pre-train them in January.  
**Expected Impact:** Prevent volume-driven breach spikes during peak months.

### Recommendation 4 — Night Shift Reinforcement 🌙
**Action:** Add 2 agents per Night shift specifically for Critical and High priority tickets. Night tickets currently wait for Morning shift handover.  
**Expected Impact:** Reduce overnight breach rate by ~35%.

### Recommendation 5 — Agent Performance Coaching 🎓
**Action:** Identify bottom 20% agents by breach rate quarterly. Provide targeted training, shadowing high-performers, and weekly 1:1 reviews.  
**Expected Impact:** Gradually move underperforming agents toward average breach rates.

### Recommendation 6 — Improve Portal Experience 🖥️
**Action:** Add AI-based ticket auto-routing on the Portal channel so tickets are assigned instantly rather than queuing in a pool.  
**Expected Impact:** Reduce Portal ticket first-response time from 3.8 hrs to < 1 hr.

---

## 4. Conclusion

The 53% SLA breach rate is unacceptable by industry standards and directly harms customer satisfaction and contract compliance. The root causes are identifiable and fixable: understaffed critical response, poor overnight coverage, and reactive (not proactive) escalation. Implementing the six recommendations above — particularly Recommendations 1, 2, and 3 — could reduce the breach rate to below 25% within two quarters.

---

*Report prepared for academic submission — Project DA-48, Data Analytics Program*
