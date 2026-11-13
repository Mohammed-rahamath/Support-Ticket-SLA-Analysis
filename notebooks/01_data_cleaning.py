"""
DA-48: Support Ticket & SLA Analysis
Script: 01_data_cleaning.py
Purpose: Load raw ticket data, identify and fix quality issues, save cleaned output.
"""

import os
import shutil
import pandas as pd
import numpy as np

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR    = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR  = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(CLEAN_DIR, exist_ok=True)

RAW_TICKETS = os.path.join(RAW_DIR, "tickets_raw.csv")
OUT_TICKETS = os.path.join(CLEAN_DIR, "tickets_cleaned.csv")

# ─── Load ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(RAW_TICKETS)
shape_before = df.shape
print(f"\n{'='*60}")
print(f"  DA-48 Data Cleaning  |  01_data_cleaning.py")
print(f"{'='*60}")
print(f"\n[LOAD]  Raw tickets shape: {shape_before[0]} rows × {shape_before[1]} cols")

# ─── Issue Detection ──────────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print("  ISSUE DETECTION")
print(f"{'─'*60}")

# 1. Null agent_id
null_agent_mask  = df["agent_id"].isna()
null_agent_count = null_agent_mask.sum()
print(f"[CHECK] Null agent_id:          {null_agent_count} rows")

# 2. Duplicate ticket_id
dup_mask  = df.duplicated(subset=["ticket_id"], keep="first")
dup_count = dup_mask.sum()
print(f"[CHECK] Duplicate ticket_id:    {dup_count} rows")

# 3. Inconsistent priority casing
priority_values = df["priority"].dropna().unique().tolist()
bad_case_mask  = df["priority"].notna() & (df["priority"] != df["priority"].str.title())
bad_case_count = bad_case_mask.sum()
print(f"[CHECK] Priority values found:  {sorted(priority_values)}")
print(f"[CHECK] Non-title-case rows:    {bad_case_count} rows")

# 4. Outlier resolution_time_hrs > 500
outlier_mask  = df["resolution_time_hrs"] > 500
outlier_count = outlier_mask.sum()
print(f"[CHECK] resolution_time_hrs>500:{outlier_count} rows")

# ─── Fixes ────────────────────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print("  APPLYING FIXES")
print(f"{'─'*60}")

# Fix 1: Fill null agent_id with mode
agent_mode = df["agent_id"].mode()[0]
df["agent_id"] = df["agent_id"].fillna(agent_mode)
print(f"[FIX 1] Filled {null_agent_count} null agent_id(s) with mode → {agent_mode}")

# Fix 2: Remove duplicate ticket_id rows (keep first)
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
print(f"[FIX 2] Removed {dup_count} duplicate ticket row(s); kept first occurrence")

# Fix 3: Standardize priority to title case
df["priority"] = df["priority"].str.strip().str.title()
print(f"[FIX 3] Standardized priority to title case (Critical/High/Medium/Low)")

# Fix 4: Cap resolution_time_hrs > 200 → NaN, then drop those rows
cap_mask  = df["resolution_time_hrs"] > 200
cap_count = cap_mask.sum()
df.loc[cap_mask, "resolution_time_hrs"] = np.nan
rows_before_drop = len(df)
df = df.dropna(subset=["resolution_time_hrs"])
rows_dropped = rows_before_drop - len(df)
print(f"[FIX 4] Capped {cap_count} resolution_time_hrs>200 → NaN, dropped {rows_dropped} row(s)")

# Fix 5: Recalculate sla_breached based on cleaned resolution_time_hrs
df["sla_breached"] = (df["resolution_time_hrs"] > df["sla_target_hours"]).astype(int)
print(f"[FIX 5] Recalculated sla_breached (1 if resolution_time_hrs > sla_target_hours)")

# ─── Summary ──────────────────────────────────────────────────────────────────
shape_after = df.shape
print(f"\n{'─'*60}")
print("  CLEANING LOG SUMMARY")
print(f"{'─'*60}")
print(f"  Rows before cleaning  : {shape_before[0]}")
print(f"  Rows after  cleaning  : {shape_after[0]}")
print(f"  Cols unchanged        : {shape_after[1]}")
print(f"  ── Issues Found & Fixed ──────────────────────")
print(f"  Null agent_id filled  : {null_agent_count}")
print(f"  Duplicates removed    : {dup_count}")
print(f"  Priority rows fixed   : {bad_case_count}")
print(f"  Outlier rows dropped  : {rows_dropped}  (resolution_time_hrs > 200)")
print(f"  sla_breached recalc   : Yes (all non-null rows)")
print(f"{'─'*60}")
print(f"\n[SHAPE] Before → {shape_before}   |   After → {shape_after}\n")

# ─── Save cleaned tickets ────────────────────────────────────────────────────
df.to_csv(OUT_TICKETS, index=False)
print(f"[SAVE] tickets_cleaned.csv  → {OUT_TICKETS}")

# ─── Copy already-clean reference files ───────────────────────────────────────
for fname in ["agents.csv", "categories.csv", "customers.csv"]:
    src = os.path.join(RAW_DIR, fname)
    dst = os.path.join(CLEAN_DIR, fname)
    shutil.copy2(src, dst)
    print(f"[COPY] {fname:<20} → {dst}")

print(f"\n{'='*60}")
print("  Cleaning complete.")
print(f"{'='*60}\n")
