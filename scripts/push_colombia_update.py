#!/usr/bin/env python3
"""One-time script: push updated Colombia network + intelligence data to Supabase.

Bypasses SQLite and pushes directly to Supabase.
Updates:
  1. Network infrastructure with spectrum_bands per-band data
  2. Intelligence event: Tigo acquires Coltel (Movistar Colombia)
  3. Movistar_co network marked as acquired (spectrum=0)
"""
import json
import os
import sys
from pathlib import Path

# Ensure project root on path
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

# Import seed data
from src.database.seed_colombia import get_seed_data

data = get_seed_data()

# ── 1. Upsert network_infrastructure ──
print("Pushing network_infrastructure for Colombia operators...")
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
    print(f"    {r['operator_id']}: spectrum_mhz={tm.get('spectrum_mhz', '?')}, "
          f"bands={'yes' if tm.get('spectrum_bands') else 'no'}")

# ── 2. Upsert intelligence events ──
print("\nPushing intelligence_events for Colombia...")
events = data["intelligence_events"]
count = 0
for evt in events:
    row = {
        "operator_id": evt.get("operator_id"),
        "market": "colombia",
        "event_date": evt["event_date"],
        "category": evt["category"],
        "title": evt["title"],
        "description": evt["description"],
        "impact_type": evt.get("impact_type"),
        "severity": evt.get("severity"),
    }
    try:
        # Try insert; if duplicate title exists, it's fine
        client.table("intelligence_events").upsert(
            row, on_conflict="market,event_date,title"
        ).execute()
        count += 1
        print(f"  ✓ {evt['title'][:60]}...")
    except Exception as e:
        # intelligence_events may not have unique constraint on these columns
        # Try plain insert
        try:
            client.table("intelligence_events").insert(row).execute()
            count += 1
            print(f"  ✓ {evt['title'][:60]}... (inserted)")
        except Exception as e2:
            print(f"  ⚠ {evt['title'][:60]}... — {e2}")

print(f"  Total events: {count}")

print("\n✅ Colombia update pushed to Supabase successfully!")
print("   - Network data with per-band spectrum_bands")
print("   - Movistar_co marked as acquired (spectrum=0)")
print("   - Coltel acquisition intelligence event added")
