#!/usr/bin/env python3
"""Verification script for the data layer (no pytest dependency)."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database.period_utils import PeriodConverter, get_converter
from datetime import date

errors = []

def check(desc, condition):
    if not condition:
        errors.append(desc)
        print(f"  FAIL: {desc}")
    else:
        print(f"  OK:   {desc}")

print("=" * 60)
print("1. Period Converter Tests")
print("=" * 60)

vf = PeriodConverter(fiscal_year_start_month=4, fiscal_year_label="FY", quarter_naming="fiscal")
dt = PeriodConverter(fiscal_year_start_month=1, fiscal_year_label="", quarter_naming="calendar")

pi = vf.to_calendar_quarter("Q3 FY26")
check("VF Q3 FY26 -> CQ4_2025", pi.calendar_quarter == "CQ4_2025")
check("VF Q3 FY26 start date", pi.period_start == date(2025, 10, 1))
check("VF Q3 FY26 end date", pi.period_end == date(2025, 12, 31))

pi = vf.to_calendar_quarter("Q1 FY26")
check("VF Q1 FY26 -> CQ2_2025", pi.calendar_quarter == "CQ2_2025")
check("VF Q1 FY26 start date", pi.period_start == date(2025, 4, 1))
check("VF Q1 FY26 end date", pi.period_end == date(2025, 6, 30))

pi = vf.to_calendar_quarter("Q4 FY26")
check("VF Q4 FY26 -> CQ1_2026", pi.calendar_quarter == "CQ1_2026")
check("VF Q4 FY26 start date", pi.period_start == date(2026, 1, 1))
check("VF Q4 FY26 end date", pi.period_end == date(2026, 3, 31))

pi = vf.to_calendar_quarter("Q2 FY25")
check("VF Q2 FY25 -> CQ3_2024", pi.calendar_quarter == "CQ3_2024")

pi = dt.to_calendar_quarter("Q4 2025")
check("DT Q4 2025 -> CQ4_2025", pi.calendar_quarter == "CQ4_2025")

pi = dt.to_calendar_quarter("Q1 2025")
check("DT Q1 2025 -> CQ1_2025", pi.calendar_quarter == "CQ1_2025")

# Round trips
result = vf.from_calendar_quarter("CQ4_2025")
check("CQ4_2025 -> Q3 FY26 (VF)", result == "Q3 FY26")

result = vf.from_calendar_quarter("CQ2_2025")
check("CQ2_2025 -> Q1 FY26 (VF)", result == "Q1 FY26")

result = vf.from_calendar_quarter("CQ1_2026")
check("CQ1_2026 -> Q4 FY26 (VF)", result == "Q4 FY26")

# Full round trip
for q_str in ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26"]:
    pi = vf.to_calendar_quarter(q_str)
    rt = vf.from_calendar_quarter(pi.calendar_quarter)
    check(f"Round trip {q_str} -> {pi.calendar_quarter} -> {rt}", rt == q_str)

# Timeline
timeline = dt.generate_timeline(n_quarters=8, end_cq="CQ4_2025")
check("Timeline has 8 items", len(timeline) == 8)
check("Timeline starts CQ1_2024", timeline[0] == "CQ1_2024")
check("Timeline ends CQ4_2025", timeline[-1] == "CQ4_2025")

# get_converter
conv = get_converter("vodafone_germany")
check("get_converter VF has fy_start=4", conv.fy_start_month == 4)
conv = get_converter("deutsche_telekom")
check("get_converter DT has fy_start=1", conv.fy_start_month == 1)
conv = get_converter("unknown")
check("get_converter unknown defaults to fy_start=1", conv.fy_start_month == 1)

# 8Q alignment
print("\n" + "=" * 60)
print("2. 8Q Vodafone-Calendar alignment")
print("=" * 60)
vf_quarters = ["Q4 FY24","Q1 FY25","Q2 FY25","Q3 FY25","Q4 FY25","Q1 FY26","Q2 FY26","Q3 FY26"]
expected_cqs = ["CQ1_2024","CQ2_2024","CQ3_2024","CQ4_2024","CQ1_2025","CQ2_2025","CQ3_2025","CQ4_2025"]
vf_conv = get_converter("vodafone_germany")
for vq, eq in zip(vf_quarters, expected_cqs):
    pi = vf_conv.to_calendar_quarter(vq)
    check(f"{vq} -> {eq}", pi.calendar_quarter == eq)

print("\n" + "=" * 60)
print("3. Database Tests")
print("=" * 60)

from src.database.db import TelecomDatabase

db = TelecomDatabase(":memory:")
db.init()

# Check tables
cursor = db.conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]
expected_tables = ["competitive_scores","data_provenance","earnings_call_highlights","executives",
                   "financial_quarterly","intelligence_events","macro_environment",
                   "network_infrastructure","operators","source_registry","subscriber_quarterly",
                   "tariffs","user_feedback"]
for t in expected_tables:
    check(f"Table {t} exists", t in tables)

# Operator CRUD
db.upsert_operator("vf", display_name="VF", country="DE", market="germany")
ops = db.get_operators_in_market("germany")
check("1 operator in germany", len(ops) == 1)
check("Operator is vf", ops[0]["operator_id"] == "vf")

# Financial
db.upsert_operator("vodafone_germany", display_name="VF Germany", country="DE", market="germany",
                    fiscal_year_start_month=4, fiscal_year_label="FY", quarter_naming="fiscal")
db.upsert_financial("vodafone_germany", "Q3 FY26", {"total_revenue": 3092, "ebitda": 1120})
data = db.get_financial_timeseries("vodafone_germany", n_quarters=8, end_cq="CQ4_2025")
check("1 financial record", len(data) == 1)
check("Revenue is 3092", data[0]["total_revenue"] == 3092)
check("CQ is CQ4_2025", data[0]["calendar_quarter"] == "CQ4_2025")

# Subscriber
db.upsert_subscriber("vodafone_germany", "Q3 FY26", {"mobile_total_k": 32500, "broadband_total_k": 9940})
data = db.get_subscriber_timeseries("vodafone_germany", n_quarters=8, end_cq="CQ4_2025")
check("1 subscriber record", len(data) == 1)
check("Mobile total is 32500k", data[0]["mobile_total_k"] == 32500)

# Competitive scores
db.upsert_competitive_scores("vodafone_germany", "CQ4_2025", {"Network Coverage": 80, "Brand": 82})
scores = db.get_competitive_scores("germany", "CQ4_2025")
check("2 competitive scores", len(scores) >= 2)

# Network
db.upsert_network("vodafone_germany", "CQ4_2025", {"five_g_coverage_pct": 90, "technology_mix": {"vendor": "Ericsson"}})
net = db.get_network_data("vodafone_germany", "CQ4_2025")
check("Network 5G is 90", net["five_g_coverage_pct"] == 90)
check("Tech mix parsed", net["technology_mix"]["vendor"] == "Ericsson")

# Macro
db.upsert_macro("Germany", "CQ4_2025", {"gdp_growth_pct": 0.8})
macro = db.get_macro_data("Germany", n_quarters=4, end_cq="CQ4_2025")
check("1 macro record", len(macro) == 1)

db.close()

print("\n" + "=" * 60)
print("4. Seed Tests")
print("=" * 60)
from src.database.seed_germany import seed_all
sdb = seed_all(":memory:")

ops = sdb.get_operators_in_market("germany")
check("4 operators seeded", len(ops) == 4)

for op_id in ["vodafone_germany", "deutsche_telekom", "telefonica_o2", "one_and_one"]:
    fd = sdb.get_financial_timeseries(op_id, n_quarters=8, end_cq="CQ4_2025")
    check(f"{op_id} has 8 financial quarters", len(fd) == 8)
    sd = sdb.get_subscriber_timeseries(op_id, n_quarters=8, end_cq="CQ4_2025")
    check(f"{op_id} has 8 subscriber quarters", len(sd) == 8)

# Check VF latest values
vf_fin = sdb.get_financial_timeseries("vodafone_germany", n_quarters=1, end_cq="CQ4_2025")
check("VF Q3 FY26 revenue=3092", vf_fin[0]["total_revenue"] == 3092)
check("VF Q3 FY26 ebitda=1120", vf_fin[0]["ebitda"] == 1120)
check("VF Q3 FY26 period label=Q3 FY26", vf_fin[0]["period"] == "Q3 FY26")

# Check DT latest values
dt_fin = sdb.get_financial_timeseries("deutsche_telekom", n_quarters=1, end_cq="CQ4_2025")
check("DT latest revenue=6200", dt_fin[0]["total_revenue"] == 6200)
check("DT latest ebitda=2610", dt_fin[0]["ebitda"] == 2610)

# Calendar alignment
vf_data = sdb.get_financial_timeseries("vodafone_germany", n_quarters=8, end_cq="CQ4_2025")
dt_data = sdb.get_financial_timeseries("deutsche_telekom", n_quarters=8, end_cq="CQ4_2025")
vf_cqs = [r["calendar_quarter"] for r in vf_data]
dt_cqs = [r["calendar_quarter"] for r in dt_data]
check("VF and DT CQs align", vf_cqs == dt_cqs)

# Market comparison
comp = sdb.get_market_comparison("germany", "CQ4_2025")
check("Market comparison returns 4 operators", len(comp) == 4)
check("DT is first (highest revenue)", comp[0]["operator_id"] == "deutsche_telekom")

# Competitive scores
scores = sdb.get_competitive_scores("germany", "CQ4_2025")
check("Competitive scores seeded", len(scores) > 0)
vf_nc = [s for s in scores if s["operator_id"] == "vodafone_germany" and s["dimension"] == "Network Coverage"]
check("VF Network Coverage = 80", len(vf_nc) == 1 and vf_nc[0]["score"] == 80)

# Macro
macro = sdb.get_macro_data("Germany", n_quarters=8, end_cq="CQ4_2025")
check("8 macro records", len(macro) == 8)
check("Latest GDP growth = 0.8", macro[-1]["gdp_growth_pct"] == 0.8)

# Network
vf_net = sdb.get_network_data("vodafone_germany", "CQ4_2025")
check("VF 5G coverage = 92", vf_net["five_g_coverage_pct"] == 92)
dt_net = sdb.get_network_data("deutsche_telekom", "CQ4_2025")
check("DT 5G coverage = 97", dt_net["five_g_coverage_pct"] == 97)

# Executives
execs = sdb.get_executives("vodafone_germany")
check("VF has >= 3 executives", len(execs) >= 3)

# Market timeseries
mts = sdb.get_market_timeseries("germany", n_quarters=8, end_cq="CQ4_2025")
check("Market timeseries has 32 rows (4x8)", len(mts) == 32)

sdb.close()

print("\n" + "=" * 60)
if errors:
    print(f"FAILURES: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED!")
    sys.exit(0)
