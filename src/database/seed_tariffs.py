"""Seed tariff data for the German telecom market.

Covers 4 operators × 7 snapshot periods × 7 plan types.
Data sourced from operator websites and industry analysis (H1_2023 – H1_2026).

Historical evolution highlights:
  - H2_2023: O2 rebranded "O2 Free" → "O2 Mobile", added 5G across all plans
  - H2_2024: O2 simplified 11→6 products, launched "Grow" auto-increment
  - H1_2025: DT doubled MagentaMobil S/M/L data allowances, same prices
  - 5G premium eroded from ~+16% (H1_2023) to ~0% (H1_2026) — now standard
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def seed_tariffs(db):
    """Insert German tariff data into the database.

    Args:
        db: Initialized TelecomDatabase instance.

    Returns:
        Number of tariff records inserted.
    """
    count = 0

    for record in TARIFF_DATA:
        db.upsert_tariff(
            operator_id=record["operator_id"],
            plan_name=record["plan_name"],
            plan_type=record["plan_type"],
            snapshot_period=record["snapshot_period"],
            data={
                "plan_tier": record.get("plan_tier"),
                "monthly_price": record.get("monthly_price"),
                "data_allowance": record.get("data_allowance"),
                "speed_mbps": record.get("speed_mbps"),
                "contract_months": record.get("contract_months", 24),
                "includes_5g": record.get("includes_5g", 0),
                "technology": record.get("technology"),
                "notes": record.get("notes"),
            },
        )
        count += 1

    print(f"  Inserted {count} tariff records")
    return count


# ============================================================================
# Helper to generate tariff records across multiple snapshots
# ============================================================================

def _expand_tariffs(operator_id, plans, snapshots, defaults=None):
    """Generate tariff records for plans across multiple snapshot periods.

    Args:
        operator_id: Operator ID
        plans: List of plan dicts (must include plan_name, plan_type, plan_tier, monthly_price)
        snapshots: List of snapshot_period strings
        defaults: Optional dict of defaults to apply to all plans

    Returns:
        List of tariff record dicts
    """
    defaults = defaults or {}
    records = []
    for snap in snapshots:
        for plan in plans:
            record = {"operator_id": operator_id, "snapshot_period": snap}
            record.update(defaults)
            record.update(plan)
            records.append(record)
    return records


# ============================================================================
# Snapshot periods
# ============================================================================

ALL_SNAPSHOTS = ["H1_2023", "H2_2023", "H1_2024", "H2_2024", "H1_2025", "H2_2025", "H1_2026"]
RECENT_SNAPSHOTS = ["H2_2024", "H1_2025", "H2_2025", "H1_2026"]


# ============================================================================
# TARIFF DATA
# ============================================================================

TARIFF_DATA = []

# =======================================================================
# Vodafone Germany — Mobile Postpaid
# =======================================================================

# H1_2023 – H1_2024: Pre-5G-standard era (5G was extra cost)
TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaMobil S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 30, "data_allowance": "5GB",  "includes_5g": 0},
    {"plan_name": "GigaMobil M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 40, "data_allowance": "15GB", "includes_5g": 0},
    {"plan_name": "GigaMobil L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 50, "data_allowance": "40GB", "includes_5g": 1},
    {"plan_name": "GigaMobil XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 60, "data_allowance": "unlimited", "includes_5g": 1},
], ["H1_2023", "H2_2023", "H1_2024"], {"contract_months": 24}))

# H2_2024 – H1_2026: Restructured, 5G standard, lower prices
TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaMobil S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 25, "data_allowance": "7GB",  "includes_5g": 1},
    {"plan_name": "GigaMobil M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 33, "data_allowance": "25GB", "includes_5g": 1},
    {"plan_name": "GigaMobil L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 40, "data_allowance": "50GB", "includes_5g": 1},
    {"plan_name": "GigaMobil XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 55, "data_allowance": "unlimited", "includes_5g": 1},
], ["H2_2024", "H1_2025", "H2_2025", "H1_2026"], {"contract_months": 24}))

# =======================================================================
# Deutsche Telekom — Mobile Postpaid
# =======================================================================

# H1_2023 – H2_2024: Premium positioning
TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaMobil S", "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 40, "data_allowance": "10GB", "includes_5g": 1},
    {"plan_name": "MagentaMobil M", "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 50, "data_allowance": "20GB", "includes_5g": 1},
    {"plan_name": "MagentaMobil L", "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 60, "data_allowance": "50GB", "includes_5g": 1},
    {"plan_name": "MagentaMobil XL","plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 85, "data_allowance": "unlimited", "includes_5g": 1},
], ["H1_2023", "H2_2023", "H1_2024", "H2_2024"], {"contract_months": 24}))

# H1_2025 – H1_2026: Data doubled, same prices
TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaMobil S", "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 40, "data_allowance": "20GB", "includes_5g": 1, "notes": "Data doubled H1_2025"},
    {"plan_name": "MagentaMobil M", "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 50, "data_allowance": "40GB", "includes_5g": 1, "notes": "Data doubled H1_2025"},
    {"plan_name": "MagentaMobil L", "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 60, "data_allowance": "100GB","includes_5g": 1, "notes": "Data doubled H1_2025"},
    {"plan_name": "MagentaMobil XL","plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 85, "data_allowance": "unlimited", "includes_5g": 1},
], ["H1_2025", "H2_2025", "H1_2026"], {"contract_months": 24}))

# =======================================================================
# Telefónica O2 Germany — Mobile Postpaid
# =======================================================================

# H1_2023 – H1_2024: Pre-rebrand era ("O2 Free")
TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 Free S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 15, "data_allowance": "6GB",   "includes_5g": 0},
    {"plan_name": "O2 Free M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 25, "data_allowance": "25GB",  "includes_5g": 0},
    {"plan_name": "O2 Free L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 35, "data_allowance": "70GB",  "includes_5g": 1},
    {"plan_name": "O2 Free Unlimited", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 55, "data_allowance": "unlimited", "includes_5g": 1},
], ["H1_2023"], {"contract_months": 24}))

# H2_2023 – H1_2024: Rebranded to "O2 Mobile", added 5G to all
TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 Mobile S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 15, "data_allowance": "6GB",   "includes_5g": 1, "notes": "Rebranded from O2 Free, 5G added"},
    {"plan_name": "O2 Mobile M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 23, "data_allowance": "30GB",  "includes_5g": 1},
    {"plan_name": "O2 Mobile L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 30, "data_allowance": "100GB", "includes_5g": 1},
    {"plan_name": "O2 Mobile Unlimited", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 50, "data_allowance": "unlimited", "includes_5g": 1},
], ["H2_2023", "H1_2024"], {"contract_months": 24}))

# H2_2024 – H1_2026: Simplified lineup with "Grow" feature
TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 Mobile S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 15, "data_allowance": "10GB",  "includes_5g": 1, "notes": "Grow: auto data increase yearly"},
    {"plan_name": "O2 Mobile M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 20, "data_allowance": "60GB",  "includes_5g": 1},
    {"plan_name": "O2 Mobile L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 25, "data_allowance": "150GB", "includes_5g": 1},
    {"plan_name": "O2 Mobile Unlimited", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 60, "data_allowance": "unlimited", "includes_5g": 1},
], ["H2_2024", "H1_2025", "H2_2025", "H1_2026"], {"contract_months": 24}))

# =======================================================================
# 1&1 — Mobile Postpaid
# =======================================================================

# H1_2023 – H2_2023: MVNO phase
TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "All-Net-Flat S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 10, "data_allowance": "10GB", "includes_5g": 0},
    {"plan_name": "All-Net-Flat M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 15, "data_allowance": "20GB", "includes_5g": 0},
    {"plan_name": "All-Net-Flat L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 25, "data_allowance": "50GB", "includes_5g": 0},
    {"plan_name": "All-Net-Flat XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 35, "data_allowance": "unlimited", "includes_5g": 0},
], ["H1_2023", "H2_2023"], {"contract_months": 24}))

# H1_2024 – H1_2026: Own network with 5G
TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "All-Net-Flat S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 15, "data_allowance": "30GB",  "includes_5g": 1, "notes": "Own network + 5G"},
    {"plan_name": "All-Net-Flat M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 20, "data_allowance": "60GB",  "includes_5g": 1},
    {"plan_name": "All-Net-Flat L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 30, "data_allowance": "120GB", "includes_5g": 1},
    {"plan_name": "All-Net-Flat XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 40, "data_allowance": "unlimited", "includes_5g": 1},
], ["H1_2024", "H2_2024", "H1_2025", "H2_2025", "H1_2026"], {"contract_months": 24}))

# =======================================================================
# Mobile Prepaid — All 4 operators
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "CallYa Digital",  "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 10, "data_allowance": "15GB",  "includes_5g": 1, "contract_months": 0},
    {"plan_name": "CallYa Allnet S", "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 15, "data_allowance": "6GB",   "includes_5g": 1, "contract_months": 0},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaMobil Prepaid S", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 8, "data_allowance": "2GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "MagentaMobil Prepaid M", "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 13, "data_allowance": "5GB", "includes_5g": 1, "contract_months": 0},
    {"plan_name": "MagentaMobil Prepaid L", "plan_type": "mobile_prepaid", "plan_tier": "l", "monthly_price": 23, "data_allowance": "10GB","includes_5g": 1, "contract_months": 0},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 Prepaid S", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 5,  "data_allowance": "2GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "O2 Prepaid M", "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 10, "data_allowance": "8GB",  "includes_5g": 1, "contract_months": 0},
    {"plan_name": "O2 Prepaid L", "plan_type": "mobile_prepaid", "plan_tier": "l", "monthly_price": 15, "data_allowance": "12.5GB","includes_5g": 1, "contract_months": 0},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "1&1 Prepaid S", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 5,  "data_allowance": "3GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "1&1 Prepaid M", "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 10, "data_allowance": "10GB", "includes_5g": 1, "contract_months": 0},
], ALL_SNAPSHOTS))

# =======================================================================
# Fixed DSL — All 4 operators
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "Red Internet & Phone DSL 50",  "plan_type": "fixed_dsl", "plan_tier": "s", "monthly_price": 30, "speed_mbps": 50,  "technology": "DSL"},
    {"plan_name": "Red Internet & Phone DSL 100", "plan_type": "fixed_dsl", "plan_tier": "m", "monthly_price": 35, "speed_mbps": 100, "technology": "DSL"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaZuhause S",  "plan_type": "fixed_dsl", "plan_tier": "s", "monthly_price": 35, "speed_mbps": 16,  "technology": "DSL"},
    {"plan_name": "MagentaZuhause M",  "plan_type": "fixed_dsl", "plan_tier": "m", "monthly_price": 40, "speed_mbps": 50,  "technology": "DSL"},
    {"plan_name": "MagentaZuhause L",  "plan_type": "fixed_dsl", "plan_tier": "l", "monthly_price": 45, "speed_mbps": 100, "technology": "DSL"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 my Home S",   "plan_type": "fixed_dsl", "plan_tier": "s", "monthly_price": 25, "speed_mbps": 10,  "technology": "DSL"},
    {"plan_name": "O2 my Home M",   "plan_type": "fixed_dsl", "plan_tier": "m", "monthly_price": 30, "speed_mbps": 50,  "technology": "DSL"},
    {"plan_name": "O2 my Home L",   "plan_type": "fixed_dsl", "plan_tier": "l", "monthly_price": 35, "speed_mbps": 100, "technology": "DSL"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "1&1 DSL 50",  "plan_type": "fixed_dsl", "plan_tier": "s", "monthly_price": 30, "speed_mbps": 50,  "technology": "DSL"},
    {"plan_name": "1&1 DSL 100", "plan_type": "fixed_dsl", "plan_tier": "m", "monthly_price": 35, "speed_mbps": 100, "technology": "DSL"},
    {"plan_name": "1&1 DSL 250", "plan_type": "fixed_dsl", "plan_tier": "l", "monthly_price": 40, "speed_mbps": 250, "technology": "VDSL"},
], ALL_SNAPSHOTS))

# =======================================================================
# Fixed Cable — Vodafone + DT (cable operators)
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaZuhause 250 Kabel",  "plan_type": "fixed_cable", "plan_tier": "m",  "monthly_price": 35, "speed_mbps": 250,  "technology": "DOCSIS 3.1"},
    {"plan_name": "GigaZuhause 500 Kabel",  "plan_type": "fixed_cable", "plan_tier": "l",  "monthly_price": 40, "speed_mbps": 500,  "technology": "DOCSIS 3.1"},
    {"plan_name": "GigaZuhause 1000 Kabel", "plan_type": "fixed_cable", "plan_tier": "xl", "monthly_price": 50, "speed_mbps": 1000, "technology": "DOCSIS 3.1"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaZuhause XL Cable", "plan_type": "fixed_cable", "plan_tier": "l",  "monthly_price": 50, "speed_mbps": 250, "technology": "DOCSIS 3.1"},
], RECENT_SNAPSHOTS))

# =======================================================================
# Fixed Fiber — DT primary, Vodafone growing, O2 emerging
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaZuhause S Glasfaser",  "plan_type": "fixed_fiber", "plan_tier": "s",  "monthly_price": 40, "speed_mbps": 100,  "technology": "FTTH"},
    {"plan_name": "MagentaZuhause M Glasfaser",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 45, "speed_mbps": 250,  "technology": "FTTH"},
    {"plan_name": "MagentaZuhause L Glasfaser",  "plan_type": "fixed_fiber", "plan_tier": "l",  "monthly_price": 55, "speed_mbps": 500,  "technology": "FTTH"},
    {"plan_name": "MagentaZuhause XL Glasfaser", "plan_type": "fixed_fiber", "plan_tier": "xl", "monthly_price": 65, "speed_mbps": 1000, "technology": "FTTH"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaZuhause 250 Glasfaser",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 40, "speed_mbps": 250,  "technology": "FTTH"},
    {"plan_name": "GigaZuhause 500 Glasfaser",  "plan_type": "fixed_fiber", "plan_tier": "l",  "monthly_price": 45, "speed_mbps": 500,  "technology": "FTTH"},
    {"plan_name": "GigaZuhause 1000 Glasfaser", "plan_type": "fixed_fiber", "plan_tier": "xl", "monthly_price": 55, "speed_mbps": 1000, "technology": "FTTH"},
], RECENT_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 my Home Glasfaser M", "plan_type": "fixed_fiber", "plan_tier": "m", "monthly_price": 35, "speed_mbps": 300,  "technology": "FTTH"},
    {"plan_name": "O2 my Home Glasfaser L", "plan_type": "fixed_fiber", "plan_tier": "l", "monthly_price": 45, "speed_mbps": 600,  "technology": "FTTH"},
], RECENT_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "1&1 Glasfaser 250",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 40, "speed_mbps": 250,  "technology": "FTTH"},
    {"plan_name": "1&1 Glasfaser 1000", "plan_type": "fixed_fiber", "plan_tier": "xl", "monthly_price": 50, "speed_mbps": 1000, "technology": "FTTH"},
], RECENT_SNAPSHOTS))

# =======================================================================
# TV — All 4 operators
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaTV Net",    "plan_type": "tv", "plan_tier": "s", "monthly_price": 10, "notes": "Streaming only"},
    {"plan_name": "GigaTV Cable",  "plan_type": "tv", "plan_tier": "m", "monthly_price": 15, "notes": "Cable + streaming"},
    {"plan_name": "GigaTV Cable inkl. Netflix", "plan_type": "tv", "plan_tier": "l", "monthly_price": 25, "notes": "Cable + Netflix bundle"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaTV Flex",  "plan_type": "tv", "plan_tier": "s", "monthly_price": 10, "notes": "Streaming only"},
    {"plan_name": "MagentaTV Smart", "plan_type": "tv", "plan_tier": "m", "monthly_price": 15, "notes": "Streaming + receiver"},
    {"plan_name": "MagentaTV SmartStream", "plan_type": "tv", "plan_tier": "l", "monthly_price": 20, "notes": "Streaming + Disney+ bundle"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 TV M",  "plan_type": "tv", "plan_tier": "s", "monthly_price": 7,  "notes": "Basic IPTV"},
    {"plan_name": "O2 TV L",  "plan_type": "tv", "plan_tier": "m", "monthly_price": 10, "notes": "Extended IPTV"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "1&1 HD TV",     "plan_type": "tv", "plan_tier": "s", "monthly_price": 5,  "notes": "Basic IPTV"},
    {"plan_name": "1&1 HD TV Plus","plan_type": "tv", "plan_tier": "m", "monthly_price": 10, "notes": "Extended IPTV"},
], ALL_SNAPSHOTS))

# =======================================================================
# FMC Bundles — All 4 operators
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("vodafone_germany", [
    {"plan_name": "GigaKombi Basic",   "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 50,  "notes": "Mobile M + Cable 250, -5€ each"},
    {"plan_name": "GigaKombi Premium", "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 80,  "notes": "Mobile XL + Cable 1000 + GigaTV"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("deutsche_telekom", [
    {"plan_name": "MagentaEINS S",      "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 65,  "notes": "MagentaMobil S + MagentaZuhause S, -5€ each"},
    {"plan_name": "MagentaEINS Premium", "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 120, "notes": "MagentaMobil XL + Glasfaser XL + MagentaTV"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("telefonica_o2", [
    {"plan_name": "O2 All-in-One S", "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 35, "notes": "O2 Mobile S + O2 my Home S"},
    {"plan_name": "O2 All-in-One L", "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 60, "notes": "O2 Mobile L + O2 my Home L"},
], ALL_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("one_and_one", [
    {"plan_name": "1&1 Kombi S",  "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 35, "notes": "Mobile S + DSL 50"},
    {"plan_name": "1&1 Kombi XL", "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 60, "notes": "Mobile XL + Glasfaser 1000"},
], ALL_SNAPSHOTS))


if __name__ == "__main__":
    from src.database.db import TelecomDatabase
    from src.database.seed_germany import seed_operators

    db = TelecomDatabase("data/telecom.db")
    db.init()
    seed_operators(db)
    n = seed_tariffs(db)
    print(f"Done. Total: {n} tariff records.")
