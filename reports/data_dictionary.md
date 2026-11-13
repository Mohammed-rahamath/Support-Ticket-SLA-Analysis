# Deliverable 1: Problem Statement & Data Dictionary
**Project DA-48 | Support Ticket & SLA Analysis**  
**Student:** Mohammed Rahamath Ulla

---

## 1. Business Context

An IT support company manages thousands of customer support tickets daily across multiple categories — from network issues to software installations. SLA (Service Level Agreement) defines the maximum time within which a ticket must be resolved. When tickets exceed SLA, it impacts customer satisfaction, violates contracts, and costs the business money.

## 2. Business Question

> **"Which tickets breach SLA, and what are the root causes — by agent, category, priority, or customer segment?"**

## 3. KPIs (Key Performance Indicators)

| KPI | Definition | Target |
|-----|-----------|--------|
| **SLA Breach Rate** | (Breached tickets / Total closed tickets) × 100 | < 20% |
| **Average Resolution Time** | Mean time (hrs) from creation to resolution | Category-specific |
| **First Response Time** | Average hrs to first agent response | < 2 hrs |
| **Ticket Volume Trend** | Monthly count of incoming tickets | Monitor for spikes |
| **Agent Breach Rate** | Breaches per agent / total assigned | < 15% |
| **Customer Satisfaction Score** | Average rating (1–5) on closed tickets | > 3.5 |

---

## 4. Data Dictionary

### Table 1: `tickets_raw.csv` (5,060 rows)
| Column | Description | Data Type | Example | Notes |
|--------|-------------|-----------|---------|-------|
| ticket_id | Unique identifier for each ticket | INT | 1, 2, 3 | Primary Key |
| customer_id | References the customer who raised the ticket | INT | 755 | FK → customers |
| agent_id | References the agent assigned to the ticket | INT / NULL | 36 | FK → agents; ~2% null |
| category_id | Type of issue | INT | 1 | FK → categories |
| priority | Urgency level of the ticket | VARCHAR | Critical / High / Medium / Low | ~3% inconsistent casing |
| status | Current state of the ticket | VARCHAR | Closed / Open / Pending | — |
| channel | How ticket was raised | VARCHAR | Email / Phone / Chat / Portal | — |
| created_at | Timestamp when ticket was opened | DATETIME | 2024-01-20 10:14:03 | — |
| resolved_at | Timestamp when ticket was closed | DATETIME / NULL | 2024-01-20 15:52:27 | NULL if Open/Pending |
| first_response_hrs | Hours from creation to first agent reply | FLOAT | 2.41 | — |
| resolution_time_hrs | Total hours taken to resolve ticket | FLOAT / NULL | 5.64 | NULL if not closed |
| sla_target_hours | Maximum hours allowed for resolution (from category) | INT | 4 | Derived from categories |
| sla_breached | 1 = breached SLA, 0 = within SLA | BINARY | 1 | Computed field |
| satisfaction_score | Customer rating after resolution (1–5) | INT / NULL | 5 | NULL if not closed |

### Table 2: `agents.csv` (150 rows)
| Column | Description | Data Type | Example |
|--------|-------------|-----------|---------|
| agent_id | Unique agent identifier | INT | 1 |
| name | Agent full name | VARCHAR | Alka Loyal |
| email | Agent work email | VARCHAR | oagate@example.com |
| department | Team the agent belongs to | VARCHAR | Network Team / Help Desk / Security / SysAdmin / Desktop Support |
| shift | Working shift | VARCHAR | Morning / Afternoon / Night |
| hire_date | Date agent joined the company | DATE | 27/08/2024 |

### Table 3: `categories.csv` (5 rows)
| Column | Description | Data Type | Example |
|--------|-------------|-----------|---------|
| category_id | Unique category identifier | INT | 1 |
| category_name | Type of issue | VARCHAR | Network Connectivity |
| sla_target_hours | Maximum resolution time allowed | INT | 4 |
| priority_level | Default priority for this category | VARCHAR | Critical / High / Medium / Low |

**All 5 Categories:**
| ID | Category | SLA Target | Priority |
|----|----------|------------|----------|
| 1 | Network Connectivity | 4 hrs | Critical |
| 2 | Software Installation | 8 hrs | High |
| 3 | Hardware Repair | 24 hrs | Medium |
| 4 | Access Rights & Permissions | 48 hrs | Low |
| 5 | Email & Collaboration | 12 hrs | High |

### Table 4: `customers.csv` (1,000 rows)
| Column | Description | Data Type | Example |
|--------|-------------|-----------|---------|
| customer_id | Unique customer identifier | INT | 1 |
| name | Customer full name | VARCHAR | Aryan Parikh |
| email | Customer email | VARCHAR | anmol89@example.org |
| phone | Customer phone number | VARCHAR | 427094580 |
| city | Customer city | VARCHAR | Pune |
| state | Customer state | VARCHAR | Maharashtra |
| registration_date | When customer registered | DATE | 2023-10-19 |

---

## 5. Data Source & Licence

- **Source:** Kaggle — Customer Support Ticket Dataset  
- **URL:** https://www.kaggle.com/datasets  
- **Licence:** Community Data Licence Agreement (open use for educational purposes)
