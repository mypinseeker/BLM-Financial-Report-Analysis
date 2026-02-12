"""Seed Chile data v2: Additional intelligence events + competitor earnings highlights.

Closes the 12→36 intelligence event gap vs Germany, and adds earnings data for
Movistar, Claro, and WOM (previously only Entel had highlights).

Run:
    python3 -m src.database.seed_chile_v2
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def get_client():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        sys.exit(1)
    return create_client(url, key)


# ======================================================================
# Additional Intelligence Events (24 new events)
# ======================================================================

CHILE_ADDITIONAL_EVENTS = [
    # --- Movistar Chile events ---
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "Movistar Chile reaches 3.5M FTTH homes passed, 55% urban coverage",
        "description": "Telefonica's Movistar Chile accelerated FTTH deployment to 3.5M homes passed (55% urban), with FTTH subscriber base growing 32% YoY to 1.4M. Average speeds increased to 600 Mbps. Targets 4.5M homes by end-2026. This makes Movistar the #1 fiber operator in Chile by homes passed.",
        "severity": "high",
        "event_date": "2025-05-15",
        "source_url": "https://www.telefonica.com/en/movistar-chile-fiber-update/",
    },
    {
        "market": "chile",
        "category": "financial",
        "impact_type": "mixed",
        "title": "Movistar Chile FY2025 revenue +3.1% YoY, EBITDA margin 28.5%",
        "description": "Movistar Chile reported FY2025 revenue growth of 3.1% YoY to CLP 490B. EBITDA margin slightly declined to 28.5% (-0.3pp) due to fiber rollout costs. Mobile service revenue grew 2.8% while fixed grew 4.2%. Postpaid base grew 4.1% to 3.8M. Convergence penetration at 38%.",
        "severity": "medium",
        "event_date": "2026-01-28",
        "source_url": "https://www.telefonica.com/en/investors/movistar-chile-fy2025/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "negative",
        "title": "Movistar Chile launches 5G in 8 cities, partners with Huawei",
        "description": "Movistar Chile launched commercial 5G NSA in 8 cities using Huawei RAN equipment. Initial coverage focused on Santiago, Valparaiso, Concepcion. 5G population coverage reached 30%. Plans to migrate to 5G SA by H2 2026. 5G pricing at CLP 2,000/month premium over 4G plans.",
        "severity": "medium",
        "event_date": "2025-06-20",
        "source_url": "https://www.telefonica.com/en/movistar-chile-5g-launch/",
    },
    # --- Claro Chile events ---
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "Claro Chile announces $300M 5G and fiber expansion plan",
        "description": "América Móvil's Claro Chile committed $300M for 2025-2026 5G+FTTH expansion. Targets 1,500 new 5G sites and 500K additional fiber homes. Strategic shift from mobile-only to convergent model. Launched first triple-play bundles combining mobile, fiber, and Claro TV+.",
        "severity": "high",
        "event_date": "2025-04-01",
        "source_url": "https://www.americamovil.com/investors/claro-chile-capex-plan/",
    },
    {
        "market": "chile",
        "category": "financial",
        "impact_type": "mixed",
        "title": "Claro Chile FY2025 revenue +2.5% YoY, mobile market share stable at 10.8%",
        "description": "Claro Chile reported FY2025 revenue of CLP 300B (+2.5% YoY). Mobile subscriber base stable at 3.3M with improving postpaid mix. EBITDA margin declined to 26% due to $300M investment program. B2B segment grew 7% driven by América Móvil group enterprise contracts.",
        "severity": "medium",
        "event_date": "2026-02-01",
        "source_url": "https://www.americamovil.com/investors/claro-chile-fy2025/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "negative",
        "title": "Claro Chile deploys 5G in Santiago and 5 regional cities",
        "description": "Claro Chile activated 5G service in Santiago and 5 additional cities (Antofagasta, La Serena, Temuco, Rancagua, Iquique). Using 3.5 GHz spectrum with Nokia equipment. Population coverage at 20%. Positions as aggressive price competitor with 5G plans starting 15% below Entel.",
        "severity": "medium",
        "event_date": "2025-08-01",
        "source_url": "https://www.clarochile.cl/5g-launch/",
    },
    # --- WOM Chile events ---
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "WOM Chile post-restructuring: aggressive pricing returns to market",
        "description": "After emerging from Chapter 11 with $800M less debt, WOM Chile launched aggressive new pricing: unlimited 5G data at CLP 15,990 (30% below Entel equivalent). WOM's cost structure now significantly lower with reduced debt service. Strategy targets 8M subscriber milestone by end-2026.",
        "severity": "high",
        "event_date": "2025-11-15",
        "source_url": "https://www.wom.cl/5g-unlimited-launch/",
    },
    {
        "market": "chile",
        "category": "financial",
        "impact_type": "mixed",
        "title": "WOM Chile H2 2025 revenue +5.2% YoY, subscriber base recovers",
        "description": "WOM Chile reported H2 2025 revenue growth of 5.2% YoY following restructuring completion. Mobile subscriber base recovered to 7.5M (+3% vs pre-restructuring low). ARPU stabilized at CLP 6,800. New management targets breakeven EBITDA by Q2 2026.",
        "severity": "medium",
        "event_date": "2026-01-15",
        "source_url": "https://www.wom.cl/investors/h2-2025-results/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "mixed",
        "title": "WOM Chile accelerates 5G deployment to 25% population coverage",
        "description": "WOM Chile reached 25% 5G population coverage, up from 10% pre-restructuring. New investor group approved $80M 5G capex for 2026. Using Samsung RAN equipment. Strategy focuses on urban hotspots and FWA for residential broadband market entry.",
        "severity": "medium",
        "event_date": "2025-12-01",
        "source_url": "https://www.wom.cl/5g-coverage-update/",
    },
    # --- Market-wide / macro events ---
    {
        "market": "chile",
        "category": "regulatory",
        "impact_type": "positive",
        "title": "SUBTEL approves 700 MHz refarming for 5G rural broadband",
        "description": "SUBTEL approved the refarming of 700 MHz spectrum for 5G NR deployment in rural areas. Entel and Movistar allocated 2x10 MHz each. Expected to bring 5G broadband to 2M additional rural households by 2027. Government subsidies of $200M available for rural deployment.",
        "severity": "high",
        "event_date": "2025-10-15",
        "source_url": "https://www.subtel.gob.cl/700mhz-refarming/",
    },
    {
        "market": "chile",
        "category": "market",
        "impact_type": "positive",
        "title": "Chile digital economy grows 12% YoY, telecom infra demand surges",
        "description": "Chile's digital economy reached 8.5% of GDP in 2025, growing 12% YoY. E-commerce transactions up 25%, driving mobile data consumption +35% YoY. Data center investment reached $1.2B with Google and AWS expanding Chilean presence. Enterprise cloud adoption at 45%.",
        "severity": "medium",
        "event_date": "2025-09-01",
        "source_url": "https://www.economia.gob.cl/digital-economy-2025/",
    },
    {
        "market": "chile",
        "category": "macro",
        "impact_type": "positive",
        "title": "Chile GDP growth 2.8% in 2025, consumer spending up 3.5%",
        "description": "Chilean GDP grew 2.8% in 2025 (vs 2.1% in 2024), supported by copper exports and services sector. Consumer spending up 3.5%, benefiting telecom retail. Central bank cut rates to 5.0% from 6.5%. Inflation fell to 3.2%. Favorable macro for telecom subscriber growth and ARPU.",
        "severity": "medium",
        "event_date": "2026-01-10",
        "source_url": "https://www.bcentral.cl/web/banco-central-de-chile/gdp-2025/",
    },
    {
        "market": "chile",
        "category": "market",
        "impact_type": "positive",
        "title": "Chile mobile penetration reaches 138%, 5G users hit 4.5M",
        "description": "SUBTEL reported Chile mobile penetration at 138% with 26.8M unique subscribers. 5G users reached 4.5M (17% of mobile base). Average mobile data consumption grew to 18 GB/month (+40% YoY). Fiber broadband penetration at 65% of fixed connections.",
        "severity": "medium",
        "event_date": "2025-12-15",
        "source_url": "https://www.subtel.gob.cl/market-statistics-q3-2025/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "positive",
        "title": "Entel Chile wins SUBTEL network quality award for 5th consecutive year",
        "description": "SUBTEL awarded Entel Chile the best network quality certification for 2025, the fifth consecutive year. Entel ranked #1 in download speed (180 Mbps avg), upload speed (45 Mbps), latency (18ms), and video streaming quality. Award reinforces Entel's premium brand positioning.",
        "severity": "medium",
        "event_date": "2025-11-20",
        "source_url": "https://www.subtel.gob.cl/network-quality-awards-2025/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "mixed",
        "title": "Opensignal: Entel #1 overall, WOM gains ground in 5G experience",
        "description": "Opensignal Chile report: Entel leads in 7/10 categories including download speed, video experience, and 5G reach. WOM won 5G download speed category in Santiago. Movistar leads in WiFi experience. Claro improved most in core experience metrics (+15% YoY). Gap narrowing in key metros.",
        "severity": "medium",
        "event_date": "2025-10-01",
        "source_url": "https://www.opensignal.com/reports/2025/chile/",
    },
    {
        "market": "chile",
        "category": "market",
        "impact_type": "positive",
        "title": "Chile enterprise telecom market grows 9% YoY to CLP 380B",
        "description": "Chile enterprise telecom market grew 9% YoY to CLP 380B in 2025. Key drivers: cloud connectivity (+22%), IoT/M2M (+18%), and managed security (+30%). Mining sector accounts for 35% of enterprise spend. Entel leads with 32% share, Movistar at 28%, Claro at 22%.",
        "severity": "medium",
        "event_date": "2025-12-20",
        "source_url": "https://www.idc.com/getdoc.jsp?containerId=LA-chile-enterprise-2025",
    },
    {
        "market": "chile",
        "category": "regulatory",
        "impact_type": "mixed",
        "title": "SUBTEL mandates net neutrality enforcement for 5G network slicing",
        "description": "SUBTEL issued new rules clarifying that 5G network slicing for enterprise is exempt from net neutrality for B2B services, but consumer slicing must comply with equal treatment. Creates regulatory clarity for enterprise private 5G monetization. Consumer 5G plans cannot be speed-tiered beyond basic/premium.",
        "severity": "medium",
        "event_date": "2025-07-15",
        "source_url": "https://www.subtel.gob.cl/net-neutrality-5g-slicing/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "positive",
        "title": "Chile becomes first LATAM country with nationwide fiber backbone",
        "description": "Chile completed its nationwide fiber backbone with the Fibra Óptica Austral project connecting Punta Arenas to the national network. Total fiber backbone: 42,000 km. Every region now has 100G+ backbone capacity. Benefits all operators with lower transport costs and enables rural broadband expansion.",
        "severity": "high",
        "event_date": "2025-08-30",
        "source_url": "https://www.subtel.gob.cl/fibra-optica-austral-complete/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "GTD (regional ISP) expands fiber to 12 cities, enters mobile as MVNO",
        "description": "Regional fiber ISP GTD expanded FTTH to 12 cities (from 6), reaching 800K homes passed. Also launched mobile MVNO on Movistar's network. Convergent bundles priced 20% below big-3 operators. Growing threat in mid-size cities where Entel and Movistar have less focus.",
        "severity": "medium",
        "event_date": "2025-09-15",
        "source_url": "https://www.gtd.cl/expansion-2025/",
    },
    {
        "market": "chile",
        "category": "financial",
        "impact_type": "positive",
        "title": "Chile telecom sector capex reaches $1.8B in 2025, highest ever",
        "description": "Combined telecom capex in Chile reached $1.8B in 2025, driven by 5G deployment ($900M), FTTH expansion ($600M), and data center ($300M). Entel capex $380M (21%), Movistar $420M (23%), Claro $350M (19%), WOM $150M (8%). Industry capex/revenue at 18.5%.",
        "severity": "medium",
        "event_date": "2026-01-20",
        "source_url": "https://www.subtel.gob.cl/telecom-investment-2025/",
    },
    {
        "market": "chile",
        "category": "macro",
        "impact_type": "positive",
        "title": "Chile central bank cuts rate to 5.0%, easing operator financing costs",
        "description": "Banco Central de Chile cut the policy rate from 6.5% to 5.0% through 2025 as inflation fell to 3.2%. Lower rates reduce financing costs for operators' capex programs. Particularly benefits WOM (post-restructuring refinancing) and Claro ($300M investment plan).",
        "severity": "medium",
        "event_date": "2025-12-10",
        "source_url": "https://www.bcentral.cl/monetary-policy-december-2025/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "mixed",
        "title": "Tigo Chile MVNO launches on Entel network, targets enterprise niche",
        "description": "Tigo Chile officially launched MVNO service on Entel's network, focusing on enterprise B2B customers and Millicom's LATAM cross-border clients. Pricing at enterprise rates only, no consumer plans. Initial 15K enterprise lines migrated. Entel earns wholesale revenue per subscriber.",
        "severity": "medium",
        "event_date": "2025-10-01",
        "source_url": "https://www.millicom.com/tigo-chile-mvno-launch/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "positive",
        "title": "Chile 5G FWA subscribers reach 120K, filling rural broadband gap",
        "description": "5G Fixed Wireless Access (FWA) subscribers in Chile reached 120K across all operators. Entel leads with 50K, Movistar 35K, Claro 25K, WOM 10K. Average FWA speed: 150 Mbps. SUBTEL reports FWA addresses 40% of previously unserved rural households. Priced at CLP 19,990 (competitive with fiber).",
        "severity": "medium",
        "event_date": "2025-11-01",
        "source_url": "https://www.subtel.gob.cl/5g-fwa-statistics-2025/",
    },
    {
        "market": "chile",
        "category": "market",
        "impact_type": "positive",
        "title": "Chile ARPU stabilizes after 3-year decline, premium tier grows 15%",
        "description": "Average blended mobile ARPU in Chile stabilized at CLP 7,200 after declining 12% since WOM's entry in 2015. Premium tier (>CLP 20K) grew 15% YoY, driven by 5G adoption and larger data bundles. Convergent bundles ARPU 40% higher than standalone mobile. ARPU growth expected to resume in 2026.",
        "severity": "medium",
        "event_date": "2025-12-01",
        "source_url": "https://www.subtel.gob.cl/arpu-trends-2025/",
    },
]


# ======================================================================
# Competitor Earnings Highlights
# ======================================================================

COMPETITOR_EARNINGS_HIGHLIGHTS = [
    # --- Movistar Chile ---
    {
        "operator_id": "movistar_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "FY2025 revenue CLP 490B (+3.1% YoY). EBITDA margin 28.5% (-0.3pp). Management targets FY2026: revenue growth 3-4%, EBITDA margin 29-30% as fiber rollout costs normalize. Capex/revenue 20% in 2025, expected to decline to 17% in 2026.",
        "speaker": "Management",
        "source_url": "https://www.telefonica.com/en/investors/movistar-chile-fy2025/",
        "notes": "Margin pressure from fiber investment. Expects normalization in 2026.",
    },
    {
        "operator_id": "movistar_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_mobile",
        "highlight_type": "explanation",
        "content": "Mobile service revenue +2.8% YoY. Postpaid base grew 4.1% to 3.8M. Prepaid declining 3% YoY. 5G launched in 8 cities, 1.2M 5G-capable users. Mobile ARPU CLP 6,900 (+1.2% YoY). Convergence bundle attach rate at 38%.",
        "speaker": "Management",
        "source_url": "https://www.telefonica.com/en/investors/movistar-chile-fy2025/",
        "notes": "Mobile growth driven by postpaid migration and convergence.",
    },
    {
        "operator_id": "movistar_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_broadband",
        "highlight_type": "explanation",
        "content": "FTTH subscriber base reached 1.4M (+32% YoY), largest fiber base in Chile. Homes passed 3.5M. Fiber ARPU CLP 22,500 (25% premium over DSL). Copper sunset 50% complete. FMC penetration at 38% of broadband base. Target: 4.5M homes passed by end-2026.",
        "speaker": "Management",
        "source_url": "https://www.telefonica.com/en/investors/movistar-chile-fy2025/",
        "notes": "Fiber leadership is Movistar's key competitive advantage over Entel in fixed.",
    },
    {
        "operator_id": "movistar_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_enterprise",
        "highlight_type": "explanation",
        "content": "Enterprise revenue grew 5.2% YoY. Telefonica Tech contributes cloud and cybersecurity solutions. B2B represents 24% of total revenue. Won 5 new managed SD-WAN contracts. IoT connections grew 20% to 1.8M. Global enterprise clients served via Telefonica Group.",
        "speaker": "Management",
        "source_url": "https://www.telefonica.com/en/investors/movistar-chile-fy2025/",
        "notes": "Enterprise growing but behind Entel. Telefonica Group synergies provide differentiation.",
    },
    # --- Claro Chile ---
    {
        "operator_id": "claro_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "FY2025 revenue CLP 300B (+2.5% YoY). EBITDA margin 26% (-2pp) due to $300M investment program. Management targets FY2026: return to 28% margin as network investment delivers subscriber growth. Focus on convergent strategy to reduce mobile-only churn.",
        "speaker": "Management",
        "source_url": "https://www.americamovil.com/investors/claro-chile-fy2025/",
        "notes": "Margin sacrifice for network catch-up. Convergence strategy is late vs Entel/Movistar.",
    },
    {
        "operator_id": "claro_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_mobile",
        "highlight_type": "explanation",
        "content": "Mobile subscriber base 3.3M (stable YoY). Postpaid mix improved to 52% (from 48%). 5G launched in 6 cities with 20% population coverage. Mobile ARPU CLP 6,200 (-0.5% YoY, pressured by WOM). Launched 5G plans at 15% discount to Entel to drive adoption.",
        "speaker": "Management",
        "source_url": "https://www.americamovil.com/investors/claro-chile-fy2025/",
        "notes": "Price-aggressive 5G strategy to gain share. ARPU under pressure.",
    },
    {
        "operator_id": "claro_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_enterprise",
        "highlight_type": "explanation",
        "content": "B2B revenue grew 7% to CLP 66B, driven by América Móvil group enterprise synergies. Won contracts with 3 mining companies for connectivity services. IoT connections grew 25% to 800K. Cloud services via Claro Cloud platform growing from small base.",
        "speaker": "Management",
        "source_url": "https://www.americamovil.com/investors/claro-chile-fy2025/",
        "notes": "Enterprise is a bright spot. Mining sector is key driver.",
    },
    # --- WOM Chile ---
    {
        "operator_id": "wom_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "Post-restructuring H2 2025 revenue CLP 192B (+5.2% YoY). EBITDA margin turned positive at 8% (from -2% in H1). Subscriber base recovered to 7.5M. Management targets FY2026: breakeven EBITDA by Q2, 10% margin by Q4. Capex $150M focused on 5G.",
        "speaker": "Management",
        "source_url": "https://www.wom.cl/investors/h2-2025-results/",
        "notes": "Strong recovery post-restructuring. Debt reduction enabling competitive pricing.",
    },
    {
        "operator_id": "wom_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_mobile",
        "highlight_type": "explanation",
        "content": "Mobile subscriber base recovered to 7.5M (+3% from restructuring low). Net adds turned positive: +120K in H2 2025. ARPU CLP 6,800 (stable). Youth segment (18-30) represents 45% of base. Launched unlimited 5G at CLP 15,990, industry's lowest 5G price.",
        "speaker": "Management",
        "source_url": "https://www.wom.cl/investors/h2-2025-results/",
        "notes": "Subscriber recovery validates digital-first and price-disruptor strategy.",
    },
    {
        "operator_id": "wom_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "strategic",
        "content": "5G coverage reached 25% population (vs 10% pre-restructuring). Samsung RAN partnership for 5G expansion. Exploring FWA for residential broadband entry. Evaluating MVNO fixed broadband partnership to offer convergent bundles without own fiber network.",
        "speaker": "Management",
        "source_url": "https://www.wom.cl/investors/h2-2025-results/",
        "notes": "FWA strategy could disrupt fixed market without fiber capex. Key risk for incumbents.",
    },
    {
        "operator_id": "wom_cl",
        "calendar_quarter": "CQ3_2025",
        "segment": "chile",
        "highlight_type": "explanation",
        "content": "Q3 2025 marked first post-restructuring quarter. Revenue CLP 94B (-2% YoY due to subscriber loss during restructuring). EBITDA margin 5% (first positive quarter since Q1 2024). Opex reduced 18% via headcount optimization and vendor renegotiation.",
        "speaker": "Management",
        "source_url": "https://www.wom.cl/investors/q3-2025-results/",
        "notes": "Restructuring delivering cost efficiency. Revenue recovery expected in Q4.",
    },
]


def seed_additional_events(client):
    """Insert additional Chile intelligence events (check for duplicates by title)."""
    print("\n[1/2] Seeding additional intelligence events for Chile...")
    existing = client.table("intelligence_events").select("title").eq("market", "chile").execute()
    existing_titles = {r["title"] for r in existing.data} if existing.data else set()

    new_events = [e for e in CHILE_ADDITIONAL_EVENTS if e["title"] not in existing_titles]
    if not new_events:
        print(f"  All {len(CHILE_ADDITIONAL_EVENTS)} events already exist — skipping")
        return

    resp = client.table("intelligence_events").insert(new_events).execute()
    print(f"  Inserted {len(resp.data)} new events (skipped {len(CHILE_ADDITIONAL_EVENTS) - len(new_events)} duplicates)")


def seed_competitor_earnings(client):
    """Insert competitor earnings highlights (check for duplicates by operator+quarter+content prefix)."""
    print("\n[2/2] Seeding competitor earnings highlights...")

    operators = ["movistar_cl", "claro_cl", "wom_cl"]
    for op_id in operators:
        existing = client.table("earnings_call_highlights").select("id").eq("operator_id", op_id).execute()
        if existing.data:
            print(f"  {op_id}: already has {len(existing.data)} highlights — skipping")
            continue

        highlights = [h for h in COMPETITOR_EARNINGS_HIGHLIGHTS if h["operator_id"] == op_id]
        if highlights:
            resp = client.table("earnings_call_highlights").insert(highlights).execute()
            print(f"  {op_id}: inserted {len(resp.data)} highlights")


def main():
    print("=" * 60)
    print("  Chile Data Seed v2 — Additional Events + Competitor Earnings")
    print("=" * 60)

    client = get_client()
    seed_additional_events(client)
    seed_competitor_earnings(client)

    print("\n" + "=" * 60)
    print("  Chile v2 seed completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
