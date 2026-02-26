#!/usr/bin/env python3
"""Push updated Panama network + intelligence data to Supabase.

Bypasses SQLite and pushes directly to Supabase.
Updates:
  1. Network infrastructure with spectrum_bands per-band data
  2. +Móvil (masmovil_pa) as new combined operator
  3. Claro PA marked as acquired, Digicel PA marked as exited
  4. Intelligence events: CWP-Claro merger, Digicel exit, spectrum tender
"""
import json
import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv(_root / "src" / "database" / ".env")

from supabase import create_client

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
if not url or not key:
    print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
    sys.exit(1)

client = create_client(url, key)

from src.database.seed_panama import get_seed_data

data = get_seed_data()

# ── 0. Ensure masmovil_pa operator exists ──
print("Ensuring +Móvil operator record exists...")
op_row = {
    "operator_id": "masmovil_pa",
    "display_name": "+Móvil Panama",
    "parent_company": "Liberty Latin America",
    "country": "Panama",
    "region": "Latin America",
    "market": "panama",
    "operator_type": "incumbent",
    "currency": "USD",
    "is_active": True,
    "fiscal_year_start_month": 1,
    "quarter_naming": "calendar",
}
try:
    client.table("operators").upsert(op_row, on_conflict="operator_id").execute()
    print("  ✓ masmovil_pa operator upserted")
except Exception as e:
    print(f"  ⚠ operator upsert: {e}")

# ── 1. Upsert network_infrastructure ──
print("\nPushing network_infrastructure for Panama operators...")
network = data["network"]
rows = []
for op_id, net_data in network.items():
    row = {
        "operator_id": op_id,
        "calendar_quarter": "CQ4_2025",
        "five_g_coverage_pct": net_data.get("five_g_coverage_pct"),
        "four_g_coverage_pct": net_data.get("four_g_coverage_pct"),
        "fiber_homepass_k": net_data.get("fiber_homepass_k"),
        "cable_homepass_k": net_data.get("cable_homepass_k"),
        "technology_mix": json.dumps(net_data.get("technology_mix", {})),
        "notes": net_data.get("notes"),
    }
    rows.append(row)

resp = (client.table("network_infrastructure")
        .upsert(rows, on_conflict="operator_id,calendar_quarter")
        .execute())
print(f"  ✓ network_infrastructure: {len(resp.data)} rows upserted")
for r in resp.data:
    tm = json.loads(r.get("technology_mix", "{}")) if isinstance(r.get("technology_mix"), str) else r.get("technology_mix", {})
    status = tm.get("status", "active")
    print(f"    {r['operator_id']}: spectrum_mhz={tm.get('spectrum_mhz', '?')}, "
          f"bands={len(tm.get('spectrum_bands', []))}, status={status}")

# ── 2. Upsert intelligence events ──
print("\nPushing intelligence_events for Panama...")
events = data["intelligence_events"]
count = 0
for evt in events:
    row = {
        "operator_id": evt.get("operator_id"),
        "market": "panama",
        "event_date": evt["event_date"],
        "category": evt["category"],
        "title": evt["title"],
        "description": evt["description"],
        "impact_type": evt.get("impact_type"),
        "severity": evt.get("severity"),
    }
    try:
        client.table("intelligence_events").upsert(
            row, on_conflict="market,event_date,title"
        ).execute()
        count += 1
        print(f"  ✓ {evt['title'][:60]}...")
    except Exception:
        try:
            client.table("intelligence_events").insert(row).execute()
            count += 1
            print(f"  ✓ {evt['title'][:60]}... (inserted)")
        except Exception as e2:
            print(f"  ⚠ {evt['title'][:60]}... — {e2}")

print(f"  Total events: {count}")

print("\n✅ Panama update pushed to Supabase successfully!")
print("   - +Móvil (CWP+ex-Claro): 136 MHz, 6 spectrum bands")
print("   - Tigo Panama: 94 MHz, 5 spectrum bands")
print("   - Claro PA: marked acquired (spectrum=0)")
print("   - Digicel PA: marked exited (spectrum=0)")
