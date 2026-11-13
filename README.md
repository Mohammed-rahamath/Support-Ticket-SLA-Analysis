# DA-48: Support Ticket & SLA Analysis 🎫

**Student:** Mohammed Rahamath Ulla  
**Domain:** IT Ops & SaaS  
**Project ID:** DA-48  

---

## 📌 Business Question
> **"Which tickets breach SLA, why do they breach, and which agents, categories, or customer segments are most affected?"**

---

## 📂 Repository Structure

```
DA-48-Support-Ticket-SLA-Analysis/
│
├── data/
│   ├── raw/              ← Original downloaded datasets
│   │   ├── tickets_raw.csv
│   │   ├── agents.csv
│   │   ├── categories.csv
│   │   └── customers.csv
│   └── cleaned/          ← After data cleaning
│       └── tickets_cleaned.csv
│
├── notebooks/
│   ├── 01_data_cleaning.py    ← Data cleaning script + log
│   ├── 02_eda_analysis.py     ← Python EDA with 8 charts
│   └── charts/                ← All generated chart images
│
├── sql/
│   └── sla_analysis_queries.sql  ← 10 SQL queries
│
├── reports/
│   ├── data_dictionary.md        ← Problem statement + data dictionary
│   ├── cleaning_log.md           ← Issues found and fixed
│   └── insights_report.md        ← Findings & recommendations
│
├── dashboard/
│   └── powerbi_guide.md          ← Power BI dashboard build guide
│
├── presentation/
│   └── slide_outline.md          ← Slide-by-slide deck guide
│
└── README.md
```

---

## 🗂️ Dataset

| Table | Rows | Description |
|-------|------|-------------|
| `tickets_raw.csv` | 5,060 | Support tickets with SLA tracking |
| `agents.csv` | 150 | Support agents (name, department, shift) |
| `categories.csv` | 5 | Ticket categories with SLA targets |
| `customers.csv` | 1,000 | Customer profiles (city, state) |

**Data Source:** Kaggle — Customer Support Ticket Dataset  
**Data Period:** January 2024 – June 2025

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| Python (Pandas, Matplotlib, Seaborn) | Data cleaning + EDA |
| MySQL / PostgreSQL | SQL analysis |
| Power BI | Interactive dashboard |
| Excel | Data dictionary |
| Word / PDF | Reports |
| PowerPoint | Presentation |

---

## 📊 Key Findings

- Overall SLA breach rate: **~53%** of closed tickets
- **Network Connectivity** (4-hour SLA) has the highest breach rate
- **Critical priority** tickets are breached most frequently
- Breach spikes occur mid-year (May–June 2024)

---

## ▶️ How to Run

```bash
# 1. Data Cleaning
python notebooks/01_data_cleaning.py

# 2. EDA & Charts
python notebooks/02_eda_analysis.py

# 3. SQL — import CSVs into MySQL and run:
mysql -u root -p < sql/sla_analysis_queries.sql
```

---

## 📋 Marks Breakdown

| Deliverable | Marks |
|-------------|-------|
| Problem Statement & Data Dictionary | 10 |
| Data Cleaning & Preparation | 15 |
| SQL Analysis (10 queries) | 15 |
| Python EDA (8 charts) | 20 |
| Power BI Dashboard | 20 |
| Insights & Recommendations | 10 |
| Presentation & Viva | 10 |
| **Total** | **100** |
