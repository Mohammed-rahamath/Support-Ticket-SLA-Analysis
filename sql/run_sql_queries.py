import sqlite3
import pandas as pd
import os

base_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\DA-48-Support-Ticket-SLA-Analysis"
cleaned_dir = os.path.join(base_dir, "data", "cleaned")
results_dir = os.path.join(base_dir, "sql", "results")
os.makedirs(results_dir, exist_ok=True)

# Load data into sqlite
conn = sqlite3.connect(":memory:")

tickets = pd.read_csv(os.path.join(cleaned_dir, "tickets_cleaned.csv"))
agents = pd.read_csv(os.path.join(cleaned_dir, "agents.csv"))
categories = pd.read_csv(os.path.join(cleaned_dir, "categories.csv"))
customers = pd.read_csv(os.path.join(cleaned_dir, "customers.csv"))

tickets.to_sql("tickets", conn, index=False)
agents.to_sql("agents", conn, index=False)
categories.to_sql("categories", conn, index=False)
customers.to_sql("customers", conn, index=False)

queries = {
    "q01_overall_breach_rate": """
        SELECT COUNT(*) as total_tickets,
               SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) as breached_tickets,
               ROUND(100.0 * SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_rate_pct,
               ROUND(AVG(resolution_time_hrs), 2) as avg_resolution_hrs
        FROM tickets
        WHERE status = 'Closed';
    """,
    "q02_breach_by_priority": """
        SELECT priority,
               COUNT(*) as total_tickets,
               SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) as breached_tickets,
               ROUND(100.0 * SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_pct,
               ROUND(AVG(resolution_time_hrs), 2) as avg_resolution_hrs
        FROM tickets
        WHERE status = 'Closed'
        GROUP BY priority
        ORDER BY breach_pct DESC;
    """,
    "q03_breach_by_category": """
        SELECT c.category_name,
               c.sla_target_hours,
               COUNT(*) as total_tickets,
               SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) as breached_tickets,
               ROUND(100.0 * SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_pct,
               ROUND(AVG(t.resolution_time_hrs), 2) as avg_resolution_hrs
        FROM tickets t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.status = 'Closed'
        GROUP BY c.category_name, c.sla_target_hours
        ORDER BY breach_pct DESC;
    """,
    "q04_top10_agents_breach": """
        SELECT a.agent_id,
               a.name as agent_name,
               a.department,
               a.shift,
               COUNT(*) as total_handled,
               SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) as breached_count,
               ROUND(100.0 * SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_pct
        FROM tickets t
        JOIN agents a ON t.agent_id = a.agent_id
        WHERE t.status = 'Closed'
        GROUP BY a.agent_id, a.name, a.department, a.shift
        ORDER BY breached_count DESC
        LIMIT 10;
    """,
    "q05_monthly_ticket_volume": """
        SELECT strftime('%Y-%m', created_at) as month,
               COUNT(*) as total_tickets,
               SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) as breached_tickets,
               ROUND(100.0 * SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_pct
        FROM tickets
        WHERE status = 'Closed'
        GROUP BY month
        ORDER BY month;
    """,
    "q06_breach_by_customer_city": """
        SELECT cu.city,
               cu.state,
               COUNT(*) as total_tickets,
               SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) as breached_tickets,
               ROUND(100.0 * SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as breach_pct
        FROM tickets t
        JOIN customers cu ON t.customer_id = cu.customer_id
        WHERE t.status = 'Closed'
        GROUP BY cu.city, cu.state
        ORDER BY total_tickets DESC
        LIMIT 10;
    """,
    "q07_avg_resolution_by_dept_cte": """
        WITH dept_metrics AS (
            SELECT a.department,
                   t.resolution_time_hrs,
                   t.sla_breached
            FROM tickets t
            JOIN agents a ON t.agent_id = a.agent_id
            WHERE t.status = 'Closed'
        )
        SELECT department,
               COUNT(*) as total_tickets,
               SUM(sla_breached) as breached_tickets,
               ROUND(AVG(resolution_time_hrs), 2) as avg_resolution_hrs,
               ROUND(100.0 * SUM(sla_breached) / COUNT(*), 2) as breach_pct
        FROM dept_metrics
        GROUP BY department
        ORDER BY avg_resolution_hrs DESC;
    """,
    "q08_rank_agents_per_category_window": """
        WITH agent_cat_counts AS (
            SELECT c.category_name,
                   a.name as agent_name,
                   COUNT(*) as tickets_handled,
                   SUM(CASE WHEN t.sla_breached = 1 THEN 1 ELSE 0 END) as breaches
            FROM tickets t
            JOIN categories c ON t.category_id = c.category_id
            JOIN agents a ON t.agent_id = a.agent_id
            WHERE t.status = 'Closed'
            GROUP BY c.category_name, a.name
        )
        SELECT category_name,
               agent_name,
               tickets_handled,
               breaches,
               RANK() OVER (PARTITION BY category_name ORDER BY breaches DESC) as breach_rank
        FROM agent_cat_counts
        LIMIT 25;
    """,
    "q09_tickets_breached_recent": """
        SELECT ticket_id,
               priority,
               category_id,
               created_at,
               resolution_time_hrs,
               sla_target_hours
        FROM tickets
        WHERE sla_breached = 1
        ORDER BY created_at DESC
        LIMIT 15;
    """,
    "q10_cumulative_monthly_breaches_window": """
        WITH monthly_counts AS (
            SELECT strftime('%Y-%m', created_at) as month,
                   SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) as monthly_breaches
            FROM tickets
            WHERE status = 'Closed'
            GROUP BY month
        )
        SELECT month,
               monthly_breaches,
               SUM(monthly_breaches) OVER (ORDER BY month) as cumulative_breaches
        FROM monthly_counts
        ORDER BY month;
    """
}

print("=== EXECUTING ALL 10 SQL ANALYTICAL QUERIES ===")
for qname, qsql in queries.items():
    df_res = pd.read_sql_query(qsql, conn)
    csv_file = os.path.join(results_dir, f"{qname}.csv")
    df_res.to_csv(csv_file, index=False)
    print(f"\n[{qname.upper()}] -> Saved to {qname}.csv")
    print(df_res.head(5).to_string())

conn.close()
print("\nAll 10 SQL queries successfully executed and stored in sql/results/.")
