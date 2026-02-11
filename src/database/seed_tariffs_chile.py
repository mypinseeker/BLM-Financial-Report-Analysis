"""Seed tariff data for the Chilean telecom market.

Covers 4 operators × 3 snapshot periods × ~15 plan types.
Data sourced from operator websites, SUBTEL Chile, and industry analysis.

Snapshot periods: H2_2024, H1_2025, H2_2025

Currency: CLP (Chilean Pesos) — monthly prices.
Note: Chile has no DSL market to speak of; fixed access is FTTH or HFC cable.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def seed_tariffs_chile(db):
    """Insert Chilean tariff data into the database.

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
                "contract_months": record.get("contract_months", 0),
                "includes_5g": record.get("includes_5g", 0),
                "technology": record.get("technology"),
                "notes": record.get("notes"),
            },
        )
        count += 1

    print(f"  Inserted {count} Chile tariff records")
    return count


# ============================================================================
# Helper to generate tariff records across multiple snapshots
# ============================================================================

def _expand_tariffs(operator_id, plans, snapshots, defaults=None):
    """Generate tariff records for plans across multiple snapshot periods."""
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
# Snapshot periods — 3 recent half-year periods
# ============================================================================

CHILE_SNAPSHOTS = ["H1_2024", "H2_2024", "H1_2025", "H2_2025", "H1_2026"]


# ============================================================================
# TARIFF DATA
# ============================================================================

TARIFF_DATA = []

# =======================================================================
# Entel Chile — Mobile Postpaid (CLP/month, no contract typical in Chile)
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("entel_cl", [
    {"plan_name": "Entel Plan S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 12990, "data_allowance": "15GB",      "includes_5g": 1},
    {"plan_name": "Entel Plan M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 17990, "data_allowance": "40GB",      "includes_5g": 1},
    {"plan_name": "Entel Plan L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 24990, "data_allowance": "80GB",      "includes_5g": 1},
    {"plan_name": "Entel Plan XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 34990, "data_allowance": "unlimited", "includes_5g": 1},
], CHILE_SNAPSHOTS, {"contract_months": 0}))

# =======================================================================
# Movistar Chile — Mobile Postpaid
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("movistar_cl", [
    {"plan_name": "Movistar Plan S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 11990, "data_allowance": "12GB",      "includes_5g": 1},
    {"plan_name": "Movistar Plan M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 16990, "data_allowance": "35GB",      "includes_5g": 1},
    {"plan_name": "Movistar Plan L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 22990, "data_allowance": "70GB",      "includes_5g": 1},
    {"plan_name": "Movistar Plan XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 32990, "data_allowance": "unlimited", "includes_5g": 1},
], CHILE_SNAPSHOTS, {"contract_months": 0}))

# =======================================================================
# Claro Chile — Mobile Postpaid
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "Claro Plan S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 10990, "data_allowance": "10GB",      "includes_5g": 1},
    {"plan_name": "Claro Plan M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 15990, "data_allowance": "30GB",      "includes_5g": 1},
    {"plan_name": "Claro Plan L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 21990, "data_allowance": "60GB",      "includes_5g": 1},
    {"plan_name": "Claro Plan XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 29990, "data_allowance": "unlimited", "includes_5g": 1},
], CHILE_SNAPSHOTS, {"contract_months": 0}))

# =======================================================================
# WOM Chile — Mobile Postpaid (aggressive pricing, disruptor)
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("wom_cl", [
    {"plan_name": "WOM Plan S",  "plan_type": "mobile_postpaid", "plan_tier": "s",  "monthly_price": 7990,  "data_allowance": "15GB",      "includes_5g": 1, "notes": "Lowest price 5G in Chile"},
    {"plan_name": "WOM Plan M",  "plan_type": "mobile_postpaid", "plan_tier": "m",  "monthly_price": 11990, "data_allowance": "40GB",      "includes_5g": 1},
    {"plan_name": "WOM Plan L",  "plan_type": "mobile_postpaid", "plan_tier": "l",  "monthly_price": 16990, "data_allowance": "80GB",      "includes_5g": 1},
    {"plan_name": "WOM Plan XL", "plan_type": "mobile_postpaid", "plan_tier": "xl", "monthly_price": 22990, "data_allowance": "unlimited", "includes_5g": 1},
], CHILE_SNAPSHOTS, {"contract_months": 0}))

# =======================================================================
# Mobile Prepaid — All 4 operators
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("entel_cl", [
    {"plan_name": "Entel Prepago Basico",  "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 5990,  "data_allowance": "5GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "Entel Prepago Plus",    "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 9990,  "data_allowance": "15GB", "includes_5g": 1, "contract_months": 0},
    {"plan_name": "Entel Prepago Premium", "plan_type": "mobile_prepaid", "plan_tier": "l", "monthly_price": 14990, "data_allowance": "30GB", "includes_5g": 1, "contract_months": 0},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("movistar_cl", [
    {"plan_name": "Movistar Prepago Basico", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 4990,  "data_allowance": "4GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "Movistar Prepago Plus",   "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 8990,  "data_allowance": "12GB", "includes_5g": 1, "contract_months": 0},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "Claro Prepago Basico", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 4990, "data_allowance": "4GB",  "includes_5g": 0, "contract_months": 0},
    {"plan_name": "Claro Prepago Plus",   "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 8990, "data_allowance": "12GB", "includes_5g": 1, "contract_months": 0},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("wom_cl", [
    {"plan_name": "WOM Prepago Basico", "plan_type": "mobile_prepaid", "plan_tier": "s", "monthly_price": 3990, "data_allowance": "5GB",  "includes_5g": 0, "contract_months": 0, "notes": "Lowest prepaid in market"},
    {"plan_name": "WOM Prepago Plus",   "plan_type": "mobile_prepaid", "plan_tier": "m", "monthly_price": 6990, "data_allowance": "15GB", "includes_5g": 1, "contract_months": 0},
    {"plan_name": "WOM Prepago Max",    "plan_type": "mobile_prepaid", "plan_tier": "l", "monthly_price": 9990, "data_allowance": "30GB", "includes_5g": 1, "contract_months": 0},
], CHILE_SNAPSHOTS))

# =======================================================================
# Fixed Fiber — Entel, Movistar, ClaroVTR
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("entel_cl", [
    {"plan_name": "Entel Fibra 300",  "plan_type": "fixed_fiber", "plan_tier": "s",  "monthly_price": 17990, "speed_mbps": 300,  "technology": "FTTH"},
    {"plan_name": "Entel Fibra 600",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 22990, "speed_mbps": 600,  "technology": "FTTH"},
    {"plan_name": "Entel Fibra 1000", "plan_type": "fixed_fiber", "plan_tier": "l",  "monthly_price": 29990, "speed_mbps": 1000, "technology": "FTTH"},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("movistar_cl", [
    {"plan_name": "Movistar Fibra 200",  "plan_type": "fixed_fiber", "plan_tier": "s",  "monthly_price": 15990, "speed_mbps": 200,  "technology": "FTTH"},
    {"plan_name": "Movistar Fibra 500",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 20990, "speed_mbps": 500,  "technology": "FTTH"},
    {"plan_name": "Movistar Fibra 1000", "plan_type": "fixed_fiber", "plan_tier": "l",  "monthly_price": 27990, "speed_mbps": 1000, "technology": "FTTH"},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "ClaroVTR Fibra 200",  "plan_type": "fixed_fiber", "plan_tier": "s",  "monthly_price": 14990, "speed_mbps": 200,  "technology": "FTTH", "notes": "HFC to FTTH migration offer"},
    {"plan_name": "ClaroVTR Fibra 500",  "plan_type": "fixed_fiber", "plan_tier": "m",  "monthly_price": 19990, "speed_mbps": 500,  "technology": "FTTH"},
    {"plan_name": "ClaroVTR Fibra 1000", "plan_type": "fixed_fiber", "plan_tier": "l",  "monthly_price": 25990, "speed_mbps": 1000, "technology": "FTTH"},
], CHILE_SNAPSHOTS))

# =======================================================================
# Fixed Cable — ClaroVTR only (VTR HFC heritage)
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "ClaroVTR Cable 200",  "plan_type": "fixed_cable", "plan_tier": "s",  "monthly_price": 13990, "speed_mbps": 200,  "technology": "DOCSIS 3.1"},
    {"plan_name": "ClaroVTR Cable 500",  "plan_type": "fixed_cable", "plan_tier": "m",  "monthly_price": 18990, "speed_mbps": 500,  "technology": "DOCSIS 3.1"},
    {"plan_name": "ClaroVTR Cable 1000", "plan_type": "fixed_cable", "plan_tier": "l",  "monthly_price": 24990, "speed_mbps": 1000, "technology": "DOCSIS 3.1"},
], CHILE_SNAPSHOTS))

# =======================================================================
# TV — ClaroVTR + Movistar
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "ClaroVTR TV Base",    "plan_type": "tv", "plan_tier": "s", "monthly_price": 9990,  "notes": "Basic cable channels + streaming app"},
    {"plan_name": "ClaroVTR TV Premium", "plan_type": "tv", "plan_tier": "m", "monthly_price": 15990, "notes": "Full cable + HBO Max + Disney+"},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("movistar_cl", [
    {"plan_name": "Movistar TV Base",    "plan_type": "tv", "plan_tier": "s", "monthly_price": 8990,  "notes": "IPTV basic package"},
    {"plan_name": "Movistar TV Premium", "plan_type": "tv", "plan_tier": "m", "monthly_price": 14990, "notes": "IPTV + streaming bundles"},
], CHILE_SNAPSHOTS))

# =======================================================================
# FMC Bundles — Entel, Movistar, ClaroVTR
# =======================================================================

TARIFF_DATA.extend(_expand_tariffs("entel_cl", [
    {"plan_name": "Entel Pack Hogar",    "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 27990, "notes": "Fibra 300 + Plan M mobile, 10% bundle discount"},
    {"plan_name": "Entel Pack Premium",  "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 49990, "notes": "Fibra 1000 + Plan XL mobile, 15% bundle discount"},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("movistar_cl", [
    {"plan_name": "Movistar Pack Duo",    "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 24990, "notes": "Fibra 200 + Plan S mobile"},
    {"plan_name": "Movistar Pack Total",  "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 54990, "notes": "Fibra 1000 + Plan XL + TV Premium"},
], CHILE_SNAPSHOTS))

TARIFF_DATA.extend(_expand_tariffs("claro_cl", [
    {"plan_name": "ClaroVTR Pack Duo",    "plan_type": "fmc_bundle", "plan_tier": "s", "monthly_price": 22990, "notes": "Fibra/Cable 200 + Claro Plan S"},
    {"plan_name": "ClaroVTR Pack Total",  "plan_type": "fmc_bundle", "plan_tier": "l", "monthly_price": 49990, "notes": "Fibra 1000 + Claro Plan XL + TV Premium"},
], CHILE_SNAPSHOTS))


if __name__ == "__main__":
    from src.database.db import TelecomDatabase
    from src.database.seed_chile import seed_operators

    db = TelecomDatabase("data/telecom.db")
    db.init()
    seed_operators(db)
    n = seed_tariffs_chile(db)
    print(f"Done. Total: {n} Chile tariff records.")
