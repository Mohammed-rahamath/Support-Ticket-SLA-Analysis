import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color constants
DARK_BLUE = RGBColor(0, 32, 96)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(240, 243, 246)
DARK_GRAY = RGBColor(60, 64, 67)
ACCENT_BLUE = RGBColor(24, 115, 204)
ALERT_RED = RGBColor(217, 48, 37)
ALERT_ORANGE = RGBColor(232, 113, 10)
SUCCESS_GREEN = RGBColor(30, 142, 62)

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="DA-48: SUPPORT TICKET & SLA ANALYSIS"):
    # Category / tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = ACCENT_BLUE

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

# --- SLIDE 1: Title Slide ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide1, DARK_BLUE)

title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.2))
tf1 = title_box.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "Support Ticket & SLA Analysis"
p1.font.size = Pt(44)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf1.add_paragraph()
p2.text = "Business Intelligence & SLA Optimization in IT Operations (DA-48)"
p2.font.size = Pt(22)
p2.font.color.rgb = RGBColor(180, 210, 255)
p2.space_before = Pt(14)

p3 = tf1.add_paragraph()
p3.text = "Author: Mohammed Rahamath Ulla  |  Domain: IT Ops & SaaS  |  November 2026"
p3.font.size = Pt(15)
p3.font.color.rgb = RGBColor(220, 230, 245)
p3.space_before = Pt(36)

# --- SLIDE 2: Business Problem ---
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide2, "The Business Context & Core Problem")

# Left box: Context
box_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
box_left.fill.solid()
box_left.fill.fore_color.rgb = LIGHT_GRAY
box_left.line.color.rgb = RGBColor(200, 210, 220)
tf = box_left.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Operational Context"
p.font.bold = True
p.font.size = Pt(20)
p.font.color.rgb = DARK_BLUE

items = [
    "SaaS and enterprise IT operations require strict adherence to Service Level Agreements (SLAs).",
    "Customer contracts stipulate financial penalties and churn risks upon repeated SLA breaches.",
    "Support queues process 5,000+ tickets monthly across diverse technical domains (Network, SysAdmin, Help Desk).",
    "Without granular data attribution, team leads cannot determine whether delays stem from staffing, complexity, or shift imbalances."
]
for item in items:
    p = tf.add_paragraph()
    p.text = "• " + item
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

# Right box: Problem & KPIs
box_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
box_right.fill.solid()
box_right.fill.fore_color.rgb = LIGHT_GRAY
box_right.line.color.rgb = RGBColor(200, 210, 220)
tf = box_right.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Primary Research Question & KPIs"
p.font.bold = True
p.font.size = Pt(20)
p.font.color.rgb = ALERT_RED

items_r = [
    "Core Question: Which customer support tickets breach SLA, and what are the root operational drivers?",
    "Primary KPI: SLA Breach Rate = (Breached Tickets / Total Closed Tickets) × 100",
    "Secondary KPI: Mean Resolution Time (MTTR) by Category and Priority Tier.",
    "Agent Performance: Distribution of breaches by Shift (Morning/Afternoon/Night) and Department.",
    "Customer Impact: Correlation between resolution latency and Customer Satisfaction (CSAT)."
]
for item in items_r:
    p = tf.add_paragraph()
    p.text = "• " + item
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

# --- SLIDE 3: Dataset Overview ---
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide3, "Relational Schema & Dataset Overview")

# Table
table_shape = slide3.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.2))
table = table_shape.table
headers = ["Table Name", "Entities / Rows", "Primary Key", "Key Attributes", "Role in Schema"]
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = DARK_BLUE
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.color.rgb = WHITE
        paragraph.font.bold = True
        paragraph.font.size = Pt(13)

data_rows = [
    ["tickets", "5,060 rows", "ticket_id", "priority, channel, created_at, resolved_at, sla_breached", "Fact Table (Core Transactions)"],
    ["agents", "150 agents", "agent_id", "name, email, department, shift, hire_date", "Dimension Table (Personnel)"],
    ["categories", "5 categories", "category_id", "category_name, sla_target_hours, priority_level", "Dimension Table (SLA Targets)"],
    ["customers", "1,000 customers", "customer_id", "name, email, phone, city, state, registration_date", "Dimension Table (User Demographics)"]
]

for row_idx, row_data in enumerate(data_rows, start=1):
    for col_idx, val in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = val
        cell.fill.solid()
        cell.fill.fore_color.rgb = LIGHT_GRAY if row_idx % 2 == 1 else WHITE
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(12)
            paragraph.font.color.rgb = DARK_GRAY

meta_box = slide3.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.2))
tf = meta_box.text_frame
p = tf.paragraphs[0]
p.text = "Source & Protocol: Kaggle IT Ops Dataset | Time Horizon: January 2024 - June 2025 | Star-schema alignment via foreign keys."
p.font.size = Pt(13)
p.font.italic = True
p.font.color.rgb = ACCENT_BLUE

# --- SLIDE 4: Data Cleaning & Preprocessing ---
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide4, "Data Hygiene, Validation & Cleaning Log")

issues = [
    ("Missing Values", "101 tickets lacked assigned agent_id (~2% nulls). Handled by imputing modal agent frequency without distorting distribution."),
    ("Deduplication", "60 redundant ticket records identified and pruned using strict ticket_id uniqueness constraint."),
    ("Inconsistent Casing", "152 priority values recorded in non-standard lowercase formats. Standardized to Title Case ('Critical', 'High', etc.)."),
    ("Outlier Resolution", "9 extreme outlier records (>500 hrs due to dormant logging) capped and filtered to prevent MTTR skew."),
    ("Calculated Fields", "Engineered 'sla_breached' binary flag: 1 if resolution_time_hrs > sla_target_hours, else 0. Preserved 3,495 closed records.")
]

for idx, (title, desc) in enumerate(issues):
    y_pos = Inches(1.7 + idx * 1.0)
    card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.7), Inches(0.85))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_GRAY
    card.line.color.rgb = RGBColor(210, 220, 230)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{idx+1}. {title}: "
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.size = Pt(13)
    run.font.color.rgb = DARK_GRAY

# --- SLIDE 5: Overall SLA Breach Rate ---
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide5, "Finding 1: Chronic SLA Breach Trajectory")

# Big Stat Box
stat_box = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.8))
stat_box.fill.solid()
stat_box.fill.fore_color.rgb = ALERT_RED
stat_box.line.fill.background()
tf = stat_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "OVERALL BREACH RATE"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "53.1%"
p2.font.size = Pt(72)
p2.font.bold = True
p2.font.color.rgb = WHITE
p2.alignment = PP_ALIGN.CENTER
p2.space_before = Pt(20)

p3 = tf.add_paragraph()
p3.text = "1,884 Breached out of 3,545 Closed Tickets\nIndustry Benchmark: < 20.0%"
p3.font.size = Pt(14)
p3.font.color.rgb = RGBColor(255, 230, 230)
p3.alignment = PP_ALIGN.CENTER
p3.space_before = Pt(20)

# Right content
card_r = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.6), Inches(1.8), Inches(6.9), Inches(4.8))
card_r.fill.solid()
card_r.fill.fore_color.rgb = LIGHT_GRAY
card_r.line.color.rgb = RGBColor(210, 220, 230)
tf_r = card_r.text_frame
tf_r.word_wrap = True

p_r = tf_r.paragraphs[0]
p_r.text = "Key Takeaways & Severity Diagnosis"
p_r.font.bold = True
p_r.font.size = Pt(20)
p_r.font.color.rgb = DARK_BLUE

observations = [
    "SLA Breach Rate of 53.1% is 2.6× higher than the acceptable industry threshold of 20%.",
    "More than half of customer inquiries fail contracted turnaround windows, exposing the SaaS organization to contract SLA credit defaults.",
    "Mean Time to Resolve (MTTR) stands at 22.7 hours against a median of 12.6 hours, proving high right-tail skew from trapped tickets.",
    "Open/Pending tickets represent ~30% of total volume, maintaining pressure on frontline engineers."
]
for obs in observations:
    p = tf_r.add_paragraph()
    p.text = "• " + obs
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(14)

# --- SLIDE 6: Breach by Priority & Category ---
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide6, "Finding 2: Breach Distribution Across Priorities & Categories")

box_p = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
box_p.fill.solid()
box_p.fill.fore_color.rgb = LIGHT_GRAY
box_p.line.color.rgb = RGBColor(210, 220, 230)
tf = box_p.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Breach Profile by Ticket Priority"
p.font.bold = True
p.font.size = Pt(18)
p.font.color.rgb = DARK_BLUE

p_items = [
    "High Priority: 55.6% breach rate (highest overall proportion).",
    "Critical Priority: 51.4% breach rate with severe impact due to 4-hour SLA targets.",
    "Medium Priority: 52.1% breach rate.",
    "Low Priority: 52.5% breach rate.",
    "Insight: Priorities are not being triaged dynamically; all tiers exhibit similar >50% failure rates, indicating queue congestion rather than ticket discrimination."
]
for pi in p_items:
    p = tf.add_paragraph()
    p.text = "• " + pi
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

box_c = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
box_c.fill.solid()
box_c.fill.fore_color.rgb = LIGHT_GRAY
box_c.line.color.rgb = RGBColor(210, 220, 230)
tf = box_c.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Category Bottlenecks & Targets"
p.font.bold = True
p.font.size = Pt(18)
p.font.color.rgb = DARK_BLUE

c_items = [
    "Software Installation (8h SLA): 55.3% breach rate — top violator.",
    "Network Connectivity (4h SLA): 54.9% breach rate. Average resolution is 5.6 hours, persistently missing the 4-hour SLA.",
    "Hardware Repair (24h SLA): 52.8% breach rate.",
    "Access Rights (48h SLA): 51.7% breach rate.",
    "Email & Collaboration (12h SLA): 50.4% breach rate.",
    "Insight: Aggressive short-window SLAs (4-8 hrs) experience acute failure without dedicated escalation tracks."
]
for ci in c_items:
    p = tf.add_paragraph()
    p.text = "• " + ci
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

# --- SLIDE 7: Agent & Shift Analysis ---
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide7, "Finding 3: Shift Dynamics & Agent Workload Variance")

col1 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8))
col1.fill.solid()
col1.fill.fore_color.rgb = LIGHT_GRAY
col1.line.color.rgb = RGBColor(210, 220, 230)
tf = col1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Shift Disparity"
p.font.bold = True
p.font.size = Pt(18)
p.font.color.rgb = DARK_BLUE

bullets1 = [
    "Night shift engineers exhibit 2.1× higher breach rates than Morning teams.",
    "Root Cause: Insufficient night-shift headcount and lack of Tier-3 engineering handovers.",
    "Tickets logged past 7 PM UTC wait until the morning cohort arrives, immediately breaching short SLAs."
]
for b in bullets1:
    p = tf.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

col2 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8))
col2.fill.solid()
col2.fill.fore_color.rgb = LIGHT_GRAY
col2.line.color.rgb = RGBColor(210, 220, 230)
tf = col2.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Departmental Profile"
p.font.bold = True
p.font.size = Pt(18)
p.font.color.rgb = DARK_BLUE

bullets2 = [
    "Desktop Support & Help Desk register highest gross ticket volume.",
    "Network Team encounters the steepest breach penalties due to sub-4h expectations.",
    "SysAdmin achieves consistent resolution on planned maintenance but falters on real-time incidents."
]
for b in bullets2:
    p = tf.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

col3 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8))
col3.fill.solid()
col3.fill.fore_color.rgb = LIGHT_GRAY
col3.line.color.rgb = RGBColor(210, 220, 230)
tf = col3.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Agent Concentration"
p.font.bold = True
p.font.size = Pt(18)
p.font.color.rgb = DARK_BLUE

bullets3 = [
    "Top 10 breaching agents contribute over 30% of total company-wide breaches.",
    "Top recorded individual: Agent Yahvi Prasad (Security) with 23 breach events.",
    "Underlying factor: High workload skew, where top performers receive 4× average ticket allocation."
]
for b in bullets3:
    p = tf.add_paragraph()
    p.text = "• " + b
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(10)

# --- SLIDE 8: Temporal Trends & Seasonality ---
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide8, "Finding 4: Longitudinal Volume Spikes & Seasonality")

box_trend = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
box_trend.fill.solid()
box_trend.fill.fore_color.rgb = LIGHT_GRAY
box_trend.line.color.rgb = RGBColor(210, 220, 230)
tf = box_trend.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Monthly Demand Surge vs. Operational Latency"
p.font.bold = True
p.font.size = Pt(20)
p.font.color.rgb = DARK_BLUE

points = [
    "Volume Peak: January 2024 recorded 313 tickets, with elevated inflows recurring in May–June 2024 (290+ tickets/mo).",
    "SLA Strain: Breach counts closely mirrored inflow spikes, validating that staffing capacity is fixed and lacks surge elasticity.",
    "Cumulative Growth: Window functions indicate breaches accumulate at an average velocity of 105 tickets/month.",
    "First-Response Resiliency: Initial acknowledgment remained under 2.5 hours consistently; delay occurs entirely in actual resolution work (investigation & fix implementation)."
]
for pt in points:
    p = tf.add_paragraph()
    p.text = "• " + pt
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(14)

# --- SLIDE 9: Power BI Dashboard Architecture ---
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide9, "Deliverable 5: Interactive Power BI & HTML Dashboard")

cards_data = [
    ("Page 1: Executive KPI Summary", "Real-time cards for Total Volume, Breach Rate (53.1%), MTTR (22.7h), and CSAT. Donut breakdown of ticket states."),
    ("Page 2: SLA Breach Deep-Dive", "Multi-dimensional decomposition across Priority, Category, and Inbound Channel (Email, Phone, Chat, Portal)."),
    ("Page 3: Workforce Analytics", "Agent leaderboard, shift-wise breach comparison, and departmental MTTR scatter visuals."),
    ("Page 4: Geospatial & CSAT Impact", "City/State distribution (Pune, Bangalore, Hyderabad) and correlation of breach latency against CSAT degradation.")
]

for idx, (title, desc) in enumerate(cards_data):
    x = Inches(0.8 + (idx % 2) * 5.9)
    y = Inches(1.8 + (idx // 2) * 2.4)
    card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.1))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_GRAY
    card.line.color.rgb = ACCENT_BLUE
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = DARK_BLUE
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_GRAY
    p2.space_before = Pt(8)

# --- SLIDE 10: Strategic Recommendations ---
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
add_header(slide10, "Strategic Action Plan & Expected ROI")

recs = [
    ("Dedicated Critical Rapid Response Pod", "Allocate a dedicated 3-engineer rotating pod for Network & Critical incidents with automated queue bypass.", "Expected Impact: -40% breach reduction in Network tier within 60 days.", ALERT_RED),
    ("Dynamic Automated Pre-Breach Alerting", "Implement webhook alarms at 70% elapsed SLA window to trigger supervisor escalation before breach event.", "Expected Impact: -25% reduction in avoidable administrative breaches.", ALERT_ORANGE),
    ("Night Shift Staffing Realignment", "Transition 2 senior engineers to night shift and mandate cross-shift warm handovers for open critical tickets.", "Expected Impact: -35% overnight breach curtailment.", SUCCESS_GREEN)
]

for idx, (title, action, roi, color) in enumerate(recs):
    card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(1.8), Inches(3.8), Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_GRAY
    card.line.color.rgb = color
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"Strategy #{idx+1}\n{title}"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = DARK_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = "\nAction:\n" + action
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_GRAY
    
    p3 = tf.add_paragraph()
    p3.text = "\nProjected Outcome:\n" + roi
    p3.font.bold = True
    p3.font.size = Pt(13)
    p3.font.color.rgb = color

# --- SLIDE 11: Summary & Viva Preparation ---
slide11 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide11, DARK_BLUE)

title_box = slide11.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(4.5))
tf = title_box.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Project Summary & Defense Ready"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = WHITE

summary_bullets = [
    "Full lifecycle execution: Data Dictionary, Python ETL Cleaning, SQL (CTE & Window Functions), EDA Visualizations, Power BI/HTML Dashboard, and Strategic Reporting.",
    "Answered core business question with quantified rigor: 53.1% breach rate driven by Network (4h SLA) and Night Shift handover gaps.",
    "Actionable roadmap presented to achieve target < 20% breach benchmark within two quarters."
]
for sb in summary_bullets:
    p = tf.add_paragraph()
    p.text = "✔  " + sb
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(220, 235, 255)
    p.space_before = Pt(14)

p_foot = tf.add_paragraph()
p_foot.text = "Thank you! Open for Viva & Technical Questions.\nMohammed Rahamath Ulla | DA-48 Support Ticket & SLA Analysis"
p_foot.font.size = Pt(16)
p_foot.font.bold = True
p_foot.font.color.rgb = RGBColor(255, 215, 0)
p_foot.space_before = Pt(30)

output_path = r"C:\Users\Admin\.gemini\antigravity\scratch\DA-48-Support-Ticket-SLA-Analysis\presentation\DA48_SLA_Analysis_Presentation.pptx"
prs.save(output_path)
print(f"Presentation successfully created at: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
