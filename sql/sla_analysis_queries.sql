-- =============================================================================
-- Project  : DA-48 — Support Ticket & SLA Analysis
-- File     : sla_analysis_queries.sql
-- Database : MySQL 8.x
-- Purpose  : Answer the core business question "Which tickets breach SLA?"
--            Ten analytical queries ranging from basic aggregations to window
--            functions and CTEs, covering breach rates, trends, agent and
--            department performance, and customer geography.
-- Author   : DA-48 Analytics Team
-- =============================================================================


-- =============================================================================
-- SCHEMA REFERENCE  (CREATE TABLE statements — no sample data inserts)
-- =============================================================================

CREATE TABLE IF NOT EXISTS agents (
    agent_id    INT           NOT NULL,
    name        VARCHAR(120)  NOT NULL,
    email       VARCHAR(200)  NOT NULL,
    department  VARCHAR(80)   NOT NULL,
    shift       VARCHAR(40)   NOT NULL,
    hire_date   DATE          NOT NULL,
    PRIMARY KEY (agent_id)
);

CREATE TABLE IF NOT EXISTS categories (
    category_id      INT          NOT NULL,
    category_name    VARCHAR(100) NOT NULL,
    sla_target_hours DECIMAL(6,2) NOT NULL,
    priority_level   VARCHAR(20)  NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id       INT          NOT NULL,
    name              VARCHAR(120) NOT NULL,
    email             VARCHAR(200) NOT NULL,
    phone             VARCHAR(30),
    city              VARCHAR(80),
    state             VARCHAR(80),
    registration_date DATE         NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id            INT           NOT NULL,
    customer_id          INT           NOT NULL,
    agent_id             INT           NOT NULL,
    category_id          INT           NOT NULL,
    priority             VARCHAR(20)   NOT NULL,       -- Critical / High / Medium / Low
    status               VARCHAR(30)   NOT NULL,
    channel              VARCHAR(40),
    created_at           DATETIME      NOT NULL,
    resolved_at          DATETIME,
    first_response_hrs   DECIMAL(8,2),
    resolution_time_hrs  DECIMAL(8,2),
    sla_target_hours     DECIMAL(8,2),
    sla_breached         TINYINT(1)    NOT NULL DEFAULT 0,  -- 1 = breached, 0 = met
    satisfaction_score   DECIMAL(3,1),
    PRIMARY KEY (ticket_id),
    CONSTRAINT fk_tickets_agent    FOREIGN KEY (agent_id)    REFERENCES agents(agent_id),
    CONSTRAINT fk_tickets_category FOREIGN KEY (category_id) REFERENCES categories(category_id),
    CONSTRAINT fk_tickets_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


-- =============================================================================
-- ANALYTICAL QUERIES
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Q1: Overall SLA health — total tickets, breach count, and breach rate %
-- Business use: Executive-level snapshot of SLA compliance.
-- -----------------------------------------------------------------------------
SELECT
    COUNT(*)                                              AS total_tickets,
    SUM(sla_breached)                                     AS breached_count,
    COUNT(*) - SUM(sla_breached)                          AS met_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2)       AS breach_rate_pct
FROM tickets;


-- -----------------------------------------------------------------------------
-- Q2: SLA breach rate by ticket priority
-- Business use: Identify which priority tiers are struggling most.
-- -----------------------------------------------------------------------------
SELECT
    priority,
    COUNT(*)                                              AS total_tickets,
    SUM(sla_breached)                                     AS breached_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2)       AS breach_rate_pct
FROM tickets
GROUP BY priority
ORDER BY breach_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- Q3: Breach rate by category
-- Business use: Pinpoint problem areas by support category.
-- -----------------------------------------------------------------------------
SELECT
    c.category_name,
    c.sla_target_hours                                    AS category_sla_hours,
    COUNT(t.ticket_id)                                    AS total_tickets,
    SUM(t.sla_breached)                                   AS breached_count,
    ROUND(SUM(t.sla_breached) * 100.0 / COUNT(*), 2)     AS breach_rate_pct,
    ROUND(AVG(t.resolution_time_hrs), 2)                  AS avg_resolution_hrs
FROM tickets t
JOIN categories c ON t.category_id = c.category_id
GROUP BY c.category_id, c.category_name, c.sla_target_hours
ORDER BY breach_rate_pct DESC;


-- -----------------------------------------------------------------------------
-- Q4: Top 10 agents with the highest SLA breach count
-- Business use: Flag agents who may need coaching or workload adjustment.
-- -----------------------------------------------------------------------------
SELECT
    a.agent_id,
    a.name                                                AS agent_name,
    a.department,
    a.shift,
    COUNT(t.ticket_id)                                    AS total_tickets,
    SUM(t.sla_breached)                                   AS breached_count,
    ROUND(SUM(t.sla_breached) * 100.0 / COUNT(*), 2)     AS breach_rate_pct
FROM tickets t
JOIN agents a ON t.agent_id = a.agent_id
GROUP BY a.agent_id, a.name, a.department, a.shift
ORDER BY breached_count DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q5: Monthly ticket volume trend
-- Business use: Spot seasonal spikes and resource planning periods.
-- -----------------------------------------------------------------------------
SELECT
    DATE_FORMAT(created_at, '%Y-%m')                      AS month,
    COUNT(*)                                              AS total_tickets,
    SUM(sla_breached)                                     AS breached_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2)       AS breach_rate_pct
FROM tickets
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY month ASC;


-- -----------------------------------------------------------------------------
-- Q6: Breach rate by customer city — top 10 cities by ticket volume
-- Business use: Geographic SLA performance for regional support planning.
-- -----------------------------------------------------------------------------
SELECT
    cu.city,
    cu.state,
    COUNT(t.ticket_id)                                    AS total_tickets,
    SUM(t.sla_breached)                                   AS breached_count,
    ROUND(SUM(t.sla_breached) * 100.0 / COUNT(*), 2)     AS breach_rate_pct
FROM tickets t
JOIN customers cu ON t.customer_id = cu.customer_id
WHERE cu.city IS NOT NULL
GROUP BY cu.city, cu.state
ORDER BY total_tickets DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q7: Average resolution time by department — using a CTE
-- Business use: Compare departmental efficiency in handling tickets.
-- -----------------------------------------------------------------------------
WITH dept_metrics AS (
    SELECT
        a.department,
        t.resolution_time_hrs,
        t.sla_breached,
        t.ticket_id
    FROM tickets t
    JOIN agents a ON t.agent_id = a.agent_id
    WHERE t.resolution_time_hrs IS NOT NULL
)
SELECT
    department,
    COUNT(ticket_id)                                      AS total_tickets,
    ROUND(AVG(resolution_time_hrs), 2)                    AS avg_resolution_hrs,
    ROUND(MIN(resolution_time_hrs), 2)                    AS min_resolution_hrs,
    ROUND(MAX(resolution_time_hrs), 2)                    AS max_resolution_hrs,
    SUM(sla_breached)                                     AS breached_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2)       AS breach_rate_pct
FROM dept_metrics
GROUP BY department
ORDER BY avg_resolution_hrs DESC;


-- -----------------------------------------------------------------------------
-- Q8: Window function — RANK agents by breach count within each category
-- Business use: Identify the worst-performing agent per support category.
-- -----------------------------------------------------------------------------
SELECT
    category_name,
    agent_name,
    department,
    breached_count,
    total_tickets,
    breach_rate_pct,
    RANK() OVER (
        PARTITION BY category_name
        ORDER BY breached_count DESC
    )                                                     AS breach_rank_in_category
FROM (
    SELECT
        c.category_name,
        a.name                                            AS agent_name,
        a.department,
        COUNT(t.ticket_id)                                AS total_tickets,
        SUM(t.sla_breached)                               AS breached_count,
        ROUND(SUM(t.sla_breached) * 100.0 / COUNT(*), 2) AS breach_rate_pct
    FROM tickets t
    JOIN agents     a ON t.agent_id    = a.agent_id
    JOIN categories c ON t.category_id = c.category_id
    GROUP BY c.category_name, a.agent_id, a.name, a.department
) agent_category_summary
ORDER BY category_name, breach_rank_in_category;


-- -----------------------------------------------------------------------------
-- Q9: Tickets that breached SLA in the last 90 days
-- Business use: Recent SLA failure list for immediate remediation review.
-- -----------------------------------------------------------------------------
SELECT
    t.ticket_id,
    t.customer_id,
    cu.name                                               AS customer_name,
    cu.city,
    a.name                                                AS agent_name,
    a.department,
    c.category_name,
    t.priority,
    t.status,
    t.created_at,
    t.resolved_at,
    t.resolution_time_hrs,
    t.sla_target_hours,
    ROUND(t.resolution_time_hrs - t.sla_target_hours, 2) AS hours_over_sla
FROM tickets t
JOIN customers  cu ON t.customer_id = cu.customer_id
JOIN agents      a ON t.agent_id    = a.agent_id
JOIN categories  c ON t.category_id = c.category_id
WHERE t.sla_breached = 1
  AND t.created_at  >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
ORDER BY hours_over_sla DESC;


-- -----------------------------------------------------------------------------
-- Q10: Running cumulative breach total by month — SUM window function
-- Business use: Visualise how accumulated SLA failures grow over time.
-- -----------------------------------------------------------------------------
SELECT
    month,
    monthly_breaches,
    monthly_tickets,
    ROUND(monthly_breaches * 100.0 / monthly_tickets, 2) AS monthly_breach_rate_pct,
    SUM(monthly_breaches) OVER (
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                     AS cumulative_breach_total,
    SUM(monthly_tickets) OVER (
        ORDER BY month
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    )                                                     AS cumulative_tickets
FROM (
    SELECT
        DATE_FORMAT(created_at, '%Y-%m')                  AS month,
        COUNT(*)                                          AS monthly_tickets,
        SUM(sla_breached)                                 AS monthly_breaches
    FROM tickets
    GROUP BY DATE_FORMAT(created_at, '%Y-%m')
) monthly_summary
ORDER BY month ASC;

-- =============================================================================
-- END OF FILE
-- =============================================================================
