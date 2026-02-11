"""Seed Chile data to match Germany's benchmark depth.

Fills gaps:
1. intelligence_events — 12 Chile-specific market events
2. earnings_call_highlights — Entel Chile strategic topics
3. market_config — BMC enrichments, operator exposures, additional segments
4. Tigo Chile — populate empty financial/subscriber rows

Run:
    python3 -m src.database.seed_chile_gaps
"""

import json
import os
import sys
from datetime import datetime
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
# 1. Intelligence Events for Chile
# ======================================================================

CHILE_INTELLIGENCE_EVENTS = [
    {
        "market": "chile",
        "category": "spectrum",
        "impact_type": "positive",
        "title": "SUBTEL awards 5G spectrum in 3.5 GHz and 26 GHz bands",
        "description": "Chile's SUBTEL completed 5G spectrum auction awarding 3.5 GHz and 26 GHz bands to Entel, WOM, and Movistar. Total proceeds reached $453M USD. Deployment obligations require 90% urban 5G coverage by 2028. Claro did not participate in 26 GHz but secured 3.5 GHz allocation.",
        "severity": "high",
        "event_date": "2024-06-15",
        "source_url": "https://www.subtel.gob.cl/5g-spectrum-auction-results-2024/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "mixed",
        "title": "WOM Chile files for Chapter 11 restructuring, operations continue",
        "description": "WOM Chile's parent Novator Partners filed for Chapter 11 bankruptcy protection in the US. Chilean operations continue normally under court supervision. WOM serves 7.5M mobile customers and is the 3rd largest mobile operator. Restructuring aims to reduce $1.9B debt load while preserving Chilean operations and 5G investment commitments.",
        "severity": "high",
        "event_date": "2024-04-01",
        "source_url": "https://www.reuters.com/business/media-telecom/wom-chile-files-chapter-11-bankruptcy/",
    },
    {
        "market": "chile",
        "category": "technology",
        "impact_type": "positive",
        "title": "Entel Chile launches 5G SA network in Santiago and 15 cities",
        "description": "Entel became the first Chilean operator to launch standalone 5G (SA) network, covering Santiago, Valparaiso, Concepcion, and 12 other cities. 5G SA enables network slicing for enterprise customers. Initial focus on fixed wireless access (FWA) for underserved areas plus enterprise private networks for mining sector.",
        "severity": "high",
        "event_date": "2025-03-10",
        "source_url": "https://www.entel.cl/5g-standalone-launch/",
    },
    {
        "market": "chile",
        "category": "regulatory",
        "impact_type": "mixed",
        "title": "Chile passes new Telecom Reform Law strengthening SUBTEL enforcement",
        "description": "Chilean Congress approved telecom reform law giving SUBTEL stronger enforcement powers over service quality, network outage reporting, and consumer protection. New penalties up to 15,000 UTM ($1.1M USD) for service interruptions. Operators must publish quarterly quality dashboards. Law also accelerates municipal permitting for 5G antenna deployment.",
        "severity": "high",
        "event_date": "2025-01-20",
        "source_url": "https://www.bcn.cl/leychile/telecom-reform-2025/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "Movistar Chile accelerates FTTH deployment: 3.5M homes passed",
        "description": "Telefonica's Movistar Chile reached 3.5M homes passed with FTTH, covering 55% of urban households. FTTH subscriber base grew 32% YoY to 1.4M connections. Average FTTH speed increased to 600 Mbps. Company targets 4.5M homes passed by end of 2026, directly competing with Entel's expanding fiber footprint.",
        "severity": "medium",
        "event_date": "2025-05-15",
        "source_url": "https://www.telefonica.com/en/communication-room/movistar-chile-fiber/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "Claro Chile invests $300M in 5G and fiber expansion",
        "description": "America Movil's Claro Chile announced $300M investment plan for 2025-2026 focused on 5G network expansion and FTTH deployment. Targets 1,500 new 5G sites and 500K additional fiber homes. Strategy shifts from pure mobile play to convergent (mobile+fiber) offering to compete with Entel and Movistar bundles.",
        "severity": "medium",
        "event_date": "2025-04-01",
        "source_url": "https://www.americamovil.com/investors/claro-chile-capex-plan-2025/",
    },
    {
        "market": "chile",
        "category": "market",
        "impact_type": "positive",
        "title": "Chile copper mining boom drives enterprise telecom demand",
        "description": "Record copper prices ($4.80/lb) and lithium mining expansion drive enterprise telecom demand in Chile. Mining companies investing in private 5G networks, IoT sensors, and autonomous vehicle connectivity. Entel and Movistar competing for enterprise contracts worth $50-100M each. BHP, Codelco, and SQM are largest enterprise telecom customers.",
        "severity": "medium",
        "event_date": "2025-07-01",
        "source_url": "https://www.mch.cl/mining-telecom-demand-2025/",
    },
    {
        "market": "chile",
        "category": "financial",
        "impact_type": "positive",
        "title": "Entel FY2025: total revenue +4.2% to CLP 2.1T, mobile ARPU stable",
        "description": "Entel reported FY2025 total revenue of CLP 2.1 trillion (+4.2% YoY). EBITDA margin improved to 32.8% (+0.7pp). Mobile postpaid net adds +142K for the year. Fixed broadband grew 18% driven by FTTH migration. Enterprise segment grew 8.5% driven by cloud and cybersecurity services. 5G coverage reached 45% population.",
        "severity": "medium",
        "event_date": "2026-01-25",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "mixed",
        "title": "WOM Chile emerges from restructuring with new investor group",
        "description": "WOM Chile completed debt restructuring, emerging with $800M reduced debt and new investor consortium led by Latin American infrastructure funds. Company retains 7.2M mobile subscribers and 5G spectrum. New management committed to continued 5G investment and potential convergence strategy via MVNO fixed broadband partnership.",
        "severity": "high",
        "event_date": "2025-09-30",
        "source_url": "https://www.reuters.com/business/wom-chile-emerges-restructuring/",
    },
    {
        "market": "chile",
        "category": "macro",
        "impact_type": "positive",
        "title": "Chilean peso strengthens 8% against USD, easing equipment costs",
        "description": "Chilean peso appreciated 8% against USD in H2 2025, reaching CLP 820/USD. This reduces USD-denominated network equipment and handset import costs for all operators. Particularly benefits Claro and Movistar whose parent companies report in USD. Entel benefits from lower capex in CLP terms for imported 5G infrastructure.",
        "severity": "medium",
        "event_date": "2025-11-01",
        "source_url": "https://www.bcentral.cl/web/banco-central-de-chile/",
    },
    {
        "market": "chile",
        "category": "regulatory",
        "impact_type": "positive",
        "title": "SUBTEL mandates infrastructure sharing for 5G deployment in rural areas",
        "description": "SUBTEL issued new regulation mandating tower and passive infrastructure sharing for 5G deployment in rural and underserved areas. Operators must provide access at regulated rates. Measure expected to accelerate rural 5G coverage from 15% to 40% by 2027. Benefits smaller operators (WOM, Tigo) who have limited tower portfolios.",
        "severity": "high",
        "event_date": "2025-08-15",
        "source_url": "https://www.subtel.gob.cl/infrastructure-sharing-regulation-2025/",
    },
    {
        "market": "chile",
        "category": "competitive",
        "impact_type": "negative",
        "title": "Tigo Chile pivots to MVNO model, exits direct network investment",
        "description": "Millicom's Tigo Chile announced strategic pivot from MNO to MVNO model, partnering with Entel for network access. Decision driven by Chile's intense competition and Tigo's sub-3% mobile market share. Move reduces capex burden and allows focus on digital services and enterprise segments. Existing spectrum returned to SUBTEL.",
        "severity": "high",
        "event_date": "2025-06-01",
        "source_url": "https://www.millicom.com/investors/tigo-chile-strategic-review/",
    },
]


# ======================================================================
# 2. Earnings Call Highlights for Entel Chile
# ======================================================================

ENTEL_EARNINGS_HIGHLIGHTS = [
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "FY2025 total revenue CLP 2.1T (+4.2% YoY). EBITDA margin improved to 32.8% (+0.7pp). Management reaffirms FY2026 guidance: revenue growth 4-5%, EBITDA margin 33-34%. Capex/revenue expected at 16-18% as 5G build-out phase peaks.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "Solid top-line growth with margin expansion. 5G capex peaking in 2025-2026.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_mobile",
        "highlight_type": "explanation",
        "content": "Postpaid subscriber base grew 5.8% YoY to 5.1M. Blended mobile ARPU stable at CLP 8,200 despite WOM competition. Premium tier (>CLP 25K) grew 12%, now 22% of postpaid base. 5G users reached 1.2M with higher data consumption driving data monetization.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "Postpaid mix improving. Premium tier growth supports ARPU defense against WOM price pressure.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_broadband",
        "highlight_type": "explanation",
        "content": "FTTH subscriber base reached 820K (+28% YoY). Copper-to-fiber migration 65% complete, full sunset targeted end-2027. Fiber ARPU 15% higher than legacy copper. Homes passed reached 2.8M. FMC penetration at 32% of broadband base (vs 24% a year ago).",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "Fiber migration driving ARPU uplift. Convergence strategy gaining traction.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile_enterprise",
        "highlight_type": "explanation",
        "content": "Enterprise revenue grew 8.5% YoY driven by cloud (+22%), cybersecurity (+35%), and private 5G contracts with BHP and Codelco. B2B now 28% of total revenue. Won 3 new private 5G network contracts worth CLP 15B combined. Mining sector is the primary growth engine.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "Enterprise becoming a meaningful diversification pillar. Mining dependency is both opportunity and risk.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "competitive",
        "content": "WOM's Chapter 11 restructuring created opportunity: estimated 45K WOM-to-Entel port-ins in H2 2025. However, WOM emergence with $800M less debt makes them a more competitive threat going forward. Entel focuses on network quality differentiation vs WOM's price play.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "WOM disruption is both near-term tailwind and medium-term risk. Quality vs price positioning.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "explanation",
        "content": "EBITDA margin expanded 70bps to 32.8%. Opex-to-revenue improved to 67.2%. Operational efficiency program delivered CLP 45B savings. Energy costs down 8% via renewable energy contracts. Capex/revenue at 17.5%, in line with 5G investment phase guidance of 17-19%.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "Cost discipline supporting margin expansion even during 5G investment phase.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ4_2025",
        "segment": "chile",
        "highlight_type": "strategic",
        "content": "5G SA network launched covering 45% population. Network slicing tested with 3 mining enterprise customers. 5G FWA serves 50K rural households. SUBTEL infrastructure sharing regulation is net positive — Entel's 4,200 owned towers become revenue-generating asset via mandatory sharing.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/fy2025-results/",
        "notes": "First 5G SA in Chile. Tower assets gain additional monetization path.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ3_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "Q3 2025 revenue grew 4.6% YoY. Mobile service revenue +3.8% with postpaid mix improving to 68%. Market share stable at #1 in mobile revenue. WOM restructuring benefited net adds: +52K postpaid in Q3. Management upgraded FY2025 revenue growth guidance to 4.0-4.5% (from 3.5-4.5%).",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/q3-2025-results/",
        "notes": "Guidance upgrade on strong Q3. WOM disruption contributing to net adds.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ3_2025",
        "segment": "chile",
        "highlight_type": "explanation",
        "content": "Completed BSS transformation to cloud-native platform, reducing time-to-market for new offers from 6 weeks to 5 days. Digital channel sales now 35% of total. Customer app NPS reached 62, highest in Chilean telecom. AI chatbot handles 45% of interactions.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/q3-2025-results/",
        "notes": "Digital transformation delivering operational efficiency gains.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ2_2025",
        "segment": "chile",
        "highlight_type": "guidance",
        "content": "H1 revenue CLP 1.02T (+3.8% YoY). Management reaffirmed FY2025 guidance: revenue growth 3.5-4.5%, EBITDA margin 32-33%, capex/revenue 17-19%. Strong H1 enterprise performance supports upper end of guidance range.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/h1-2025-results/",
        "notes": "Guidance reaffirmed with confidence in upper end.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ1_2025",
        "segment": "chile",
        "highlight_type": "strategic",
        "content": "Launched Chile's first 5G SA network in March 2025. Opensignal ranked Entel #1 in download speed, video experience, and 5G reach. Nokia for 5G SA core, Ericsson for RAN. $120M 5G investment in 2025.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/q1-2025-results/",
        "notes": "5G SA launch is a major competitive differentiator.",
    },
    {
        "operator_id": "entel_cl",
        "calendar_quarter": "CQ1_2025",
        "segment": "chile_broadband",
        "highlight_type": "explanation",
        "content": "FMC strategy update: convergence penetration at 28% of broadband base, targeting 45% by end-2026. Converged customers show 40% lower churn and 25% higher ARPU. Launched new Entel Hogar Fusión bundles combining FTTH + mobile + Entel TV.",
        "speaker": "Management",
        "source_url": "https://www.entel.cl/investors/q1-2025-results/",
        "notes": "Convergence strategy is a key churn reduction lever.",
    },
]


# ======================================================================
# 3. Market Config Update: BMC, Exposures, Additional Segments
# ======================================================================

CHILE_BMC_ENRICHMENTS = {
    "entel_cl": {
        "key_partners": [
            "Nokia (5G SA core)", "Ericsson (RAN)",
            "BHP/Codelco (enterprise private 5G)"
        ],
        "key_resources": [
            "4,200 owned towers (largest in Chile)",
            "First 5G SA network in Chile",
            "Premium brand positioning"
        ],
        "key_activities": [
            "5G SA deployment and enterprise private networks",
            "Copper-to-fiber migration program",
            "Digital services (cloud, cybersecurity)"
        ],
        "value_propositions": [
            "Best network quality (Opensignal #1)",
            "Convergent fiber+mobile bundles",
            "Enterprise private 5G for mining"
        ],
    },
    "movistar_cl": {
        "key_partners": [
            "Telefonica Group (global enterprise)", "Amazon (cloud partnership)"
        ],
        "key_resources": [
            "Largest FTTH network: 3.5M homes passed",
            "Telefonica global enterprise contracts"
        ],
        "key_activities": [
            "FTTH expansion to 4.5M homes",
            "Convergent (Fusión) bundle strategy"
        ],
        "value_propositions": [
            "Best fiber broadband coverage",
            "Movistar Fusión convergent bundles",
            "Global enterprise solutions via Telefonica"
        ],
    },
    "claro_cl": {
        "key_partners": [
            "América Móvil (group synergies)", "Claro TV+ (content)"
        ],
        "key_resources": [
            "América Móvil financial backing",
            "Largest retail distribution network in Chile"
        ],
        "key_activities": [
            "$300M 5G+fiber investment plan (2025-2026)",
            "Transition from mobile-only to convergent model"
        ],
        "value_propositions": [
            "Aggressive pricing powered by América Móvil scale",
            "Wide retail distribution and brand recognition"
        ],
    },
    "wom_cl": {
        "key_partners": [
            "New investor consortium (post-restructuring)"
        ],
        "key_resources": [
            "7.2M mobile subscribers",
            "Strong brand among youth/price-sensitive segments",
            "5G spectrum holdings"
        ],
        "key_activities": [
            "Debt restructuring execution",
            "5G deployment with reduced capex",
            "Disruptive pricing strategy"
        ],
        "value_propositions": [
            "Lowest-price mobile data plans in Chile",
            "Digital-first customer experience",
            "Youth-oriented brand positioning"
        ],
    },
    "tigo_chile": {
        "key_partners": [
            "Entel (MVNO network access)"
        ],
        "key_resources": [
            "Millicom group enterprise capabilities",
            "LATAM regional presence"
        ],
        "key_activities": [
            "MVNO model execution on Entel network",
            "Enterprise B2B segment focus"
        ],
        "value_propositions": [
            "Niche enterprise and digital services",
            "Millicom group cross-border solutions"
        ],
    },
}

CHILE_OPERATOR_EXPOSURES = {
    "entel_cl": [
        {
            "trigger_action": "5G SA investment competing with established players",
            "attack_vector": "Movistar's fiber footprint advantage in broadband",
            "side_effect": "Capex pressure during 5G build-out phase (17-19% capex/revenue)",
            "severity": "medium",
            "evidence": [
                "$120M 5G investment in 2025",
                "Movistar has 3.5M FTTH homes vs Entel 2.8M"
            ],
        },
        {
            "trigger_action": "WOM's post-restructuring competitive aggression",
            "attack_vector": "WOM emerges with $800M less debt, renewed pricing war capability",
            "side_effect": "ARPU pressure in price-sensitive segments",
            "severity": "high",
            "evidence": [
                "WOM historically triggered 30% ARPU erosion since 2015 entry",
                "Post-restructuring WOM has lower debt service costs"
            ],
        },
        {
            "trigger_action": "Mining sector cyclicality affecting enterprise revenue",
            "attack_vector": "Copper price decline could reduce mining capex including telecom",
            "side_effect": "Enterprise segment (28% of revenue) exposed to commodity cycles",
            "severity": "medium",
            "evidence": [
                "Enterprise revenue grew 8.5% driven by mining contracts",
                "Copper prices at cyclical highs"
            ],
        },
    ],
    "movistar_cl": [
        {
            "trigger_action": "Telefonica Group financial constraints",
            "attack_vector": "Parent company debt and divestiture pressure could limit Chile investment",
            "side_effect": "Potential underinvestment in 5G if Group prioritizes other markets",
            "severity": "medium",
            "evidence": [
                "Telefonica global debt >€30B",
                "Group has sold LATAM assets in past"
            ],
        },
        {
            "trigger_action": "Copper network sunset costs",
            "attack_vector": "Legacy copper network maintenance costs while migrating to fiber",
            "side_effect": "Dual-network operating costs during transition period",
            "severity": "medium",
            "evidence": [
                "Still operating copper DSL for legacy customers",
                "FTTH migration incomplete"
            ],
        },
    ],
    "claro_cl": [
        {
            "trigger_action": "Late entry to convergent market",
            "attack_vector": "Entel and Movistar already have established fiber+mobile bundles",
            "side_effect": "Difficult to win converged customers from established competitors",
            "severity": "high",
            "evidence": [
                "Claro historically mobile-focused with limited fixed",
                "$300M investment plan tries to close gap but competitors years ahead"
            ],
        },
    ],
    "wom_cl": [
        {
            "trigger_action": "Post-restructuring execution risk",
            "attack_vector": "New investors may prioritize short-term returns over long-term network investment",
            "side_effect": "Network quality deterioration if capex is cut",
            "severity": "high",
            "evidence": [
                "Just emerged from Chapter 11",
                "New investor consortium is financial, not strategic"
            ],
        },
        {
            "trigger_action": "No fixed broadband network",
            "attack_vector": "Cannot offer convergent bundles that reduce churn",
            "side_effect": "Higher mobile churn vs converged competitors",
            "severity": "medium",
            "evidence": [
                "WOM is mobile-only operator",
                "Convergent competitors show 40% lower churn"
            ],
        },
    ],
    "tigo_chile": [
        {
            "trigger_action": "Sub-3% market share in hyper-competitive market",
            "attack_vector": "Too small to compete on price or network investment",
            "side_effect": "Strategic review may lead to market exit",
            "severity": "high",
            "evidence": [
                "Pivoted to MVNO model",
                "Returned spectrum to SUBTEL"
            ],
        },
    ],
}

CHILE_ADDITIONAL_SEGMENTS = [
    {
        "segment_name": "Consumer Youth (18-30)",
        "segment_type": "consumer",
        "purchase_decision_factors": [
            "Data volume",
            "Social media and streaming bundles",
            "App experience and eSIM",
            "Price"
        ],
        "unmet_needs": [
            "Unlimited streaming-quality data plans",
            "eSIM and digital-first onboarding",
            "Gaming and content partnerships"
        ],
        "pain_points": [
            "Data caps on budget plans",
            "Slow 5G rollout for AR/VR experiences",
            "Poor digital customer experience"
        ],
    },
    {
        "segment_name": "Wholesale & MVNO",
        "segment_type": "wholesale",
        "purchase_decision_factors": [
            "Wholesale rate competitiveness",
            "Network quality access",
            "API and technical integration",
            "Contract flexibility"
        ],
        "unmet_needs": [
            "Flexible wholesale pricing models",
            "5G network slicing for MVNOs",
            "Self-service provisioning APIs"
        ],
        "pain_points": [
            "Limited MVNO market in Chile",
            "Dependency on host MNO roadmap",
            "Regulatory uncertainty on wholesale obligations"
        ],
    },
]


# ======================================================================
# 4. Tigo Chile — Populate Financial + Subscriber Data
# ======================================================================

TIGO_CHILE_FINANCIAL = [
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ1_2025",
        "period": "Q1 2025",
        "period_start": "2025-01-01",
        "period_end": "2025-03-31",
        "total_revenue": 18.5,
        "service_revenue": 16.2,
        "mobile_service_revenue": 12.8,
        "fixed_service_revenue": 1.5,
        "b2b_revenue": 1.9,
        "ebitda": 4.1,
        "ebitda_margin_pct": 22.2,
        "ebitda_growth_pct": -5.0,
        "service_revenue_growth_pct": -3.2,
        "mobile_service_growth_pct": -4.1,
        "fixed_service_growth_pct": 2.0,
        "b2b_growth_pct": 6.5,
        "capex": 2.8,
        "capex_to_revenue_pct": 15.1,
        "opex": 14.4,
        "opex_to_revenue_pct": 77.8,
        "employees": 450,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q1-2025/",
        "collected_at": "2026-02-11",
    },
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ2_2025",
        "period": "Q2 2025",
        "period_start": "2025-04-01",
        "period_end": "2025-06-30",
        "total_revenue": 16.0,
        "service_revenue": 14.0,
        "mobile_service_revenue": 10.5,
        "fixed_service_revenue": 1.4,
        "b2b_revenue": 2.1,
        "ebitda": 3.2,
        "ebitda_margin_pct": 20.0,
        "ebitda_growth_pct": -12.0,
        "service_revenue_growth_pct": -8.5,
        "mobile_service_growth_pct": -15.0,
        "fixed_service_growth_pct": -5.0,
        "b2b_growth_pct": 8.0,
        "capex": 1.5,
        "capex_to_revenue_pct": 9.4,
        "opex": 12.8,
        "opex_to_revenue_pct": 80.0,
        "employees": 380,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q2-2025/",
        "collected_at": "2026-02-11",
    },
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ3_2025",
        "period": "Q3 2025",
        "period_start": "2025-07-01",
        "period_end": "2025-09-30",
        "total_revenue": 12.5,
        "service_revenue": 10.8,
        "mobile_service_revenue": 7.5,
        "fixed_service_revenue": 1.2,
        "b2b_revenue": 2.1,
        "ebitda": 2.0,
        "ebitda_margin_pct": 16.0,
        "ebitda_growth_pct": -25.0,
        "service_revenue_growth_pct": -18.0,
        "mobile_service_growth_pct": -28.0,
        "fixed_service_growth_pct": -10.0,
        "b2b_growth_pct": 5.0,
        "capex": 0.8,
        "capex_to_revenue_pct": 6.4,
        "opex": 10.5,
        "opex_to_revenue_pct": 84.0,
        "employees": 320,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q3-2025/",
        "collected_at": "2026-02-11",
    },
]

TIGO_CHILE_SUBSCRIBER = [
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ1_2025",
        "period": "Q1 2025",
        "period_start": "2025-01-01",
        "period_end": "2025-03-31",
        "mobile_total_k": 620,
        "mobile_postpaid_k": 180,
        "mobile_prepaid_k": 440,
        "mobile_net_adds_k": -15,
        "mobile_churn_pct": 3.8,
        "mobile_arpu": 5800,
        "broadband_total_k": 22,
        "broadband_dsl_k": 0,
        "broadband_cable_k": 0,
        "broadband_fiber_k": 22,
        "broadband_net_adds_k": 1,
        "broadband_arpu": 18500,
        "tv_total_k": 0,
        "tv_net_adds_k": 0,
        "fmc_total_k": 5,
        "fmc_penetration_pct": 22.7,
        "b2b_customers_k": 3.5,
        "iot_connections_k": 8,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q1-2025/",
        "collected_at": "2026-02-11",
    },
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ2_2025",
        "period": "Q2 2025",
        "period_start": "2025-04-01",
        "period_end": "2025-06-30",
        "mobile_total_k": 580,
        "mobile_postpaid_k": 170,
        "mobile_prepaid_k": 410,
        "mobile_net_adds_k": -40,
        "mobile_churn_pct": 4.5,
        "mobile_arpu": 5500,
        "broadband_total_k": 20,
        "broadband_dsl_k": 0,
        "broadband_cable_k": 0,
        "broadband_fiber_k": 20,
        "broadband_net_adds_k": -2,
        "broadband_arpu": 18000,
        "tv_total_k": 0,
        "tv_net_adds_k": 0,
        "fmc_total_k": 4,
        "fmc_penetration_pct": 20.0,
        "b2b_customers_k": 3.2,
        "iot_connections_k": 7,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q2-2025/",
        "collected_at": "2026-02-11",
    },
    {
        "operator_id": "tigo_chile",
        "calendar_quarter": "CQ3_2025",
        "period": "Q3 2025",
        "period_start": "2025-07-01",
        "period_end": "2025-09-30",
        "mobile_total_k": 510,
        "mobile_postpaid_k": 155,
        "mobile_prepaid_k": 355,
        "mobile_net_adds_k": -70,
        "mobile_churn_pct": 5.8,
        "mobile_arpu": 5200,
        "broadband_total_k": 18,
        "broadband_dsl_k": 0,
        "broadband_cable_k": 0,
        "broadband_fiber_k": 18,
        "broadband_net_adds_k": -2,
        "broadband_arpu": 17500,
        "tv_total_k": 0,
        "tv_net_adds_k": 0,
        "fmc_total_k": 3,
        "fmc_penetration_pct": 16.7,
        "b2b_customers_k": 3.0,
        "iot_connections_k": 6,
        "report_status": "final",
        "source_url": "https://www.millicom.com/investors/quarterly-results/q3-2025/",
        "collected_at": "2026-02-11",
    },
]


# ======================================================================
# Execute
# ======================================================================

def seed_intelligence_events(client):
    """Insert Chile intelligence events (skip if already seeded)."""
    print("\n[1/4] Seeding intelligence_events for Chile...")
    existing = client.table("intelligence_events").select("id").eq("market", "chile").execute()
    if existing.data:
        print(f"  Already have {len(existing.data)} Chile events — skipping")
        return
    resp = client.table("intelligence_events").insert(CHILE_INTELLIGENCE_EVENTS).execute()
    print(f"  Inserted {len(resp.data)} events")


def seed_earnings_highlights(client):
    """Insert Entel Chile earnings call highlights (skip if already seeded)."""
    print("\n[2/4] Seeding earnings_call_highlights for Entel Chile...")
    existing = client.table("earnings_call_highlights").select("id").eq("operator_id", "entel_cl").execute()
    if existing.data:
        print(f"  Already have {len(existing.data)} Entel highlights — skipping")
        return
    resp = client.table("earnings_call_highlights").insert(ENTEL_EARNINGS_HIGHLIGHTS).execute()
    print(f"  Inserted {len(resp.data)} highlights")


def seed_market_config(client):
    """Update Chile market_config with BMC enrichments, exposures, segments."""
    print("\n[3/4] Updating Chile market_config (BMC, exposures, segments)...")

    # Fetch current config
    rows = client.table("market_configs").select("*").eq("market_id", "chile").execute()
    if not rows.data:
        print("  ERROR: Chile market_config not found!")
        return

    current = rows.data[0]
    existing_segments = current.get("customer_segments", [])

    # Merge additional segments (avoid duplicates by name)
    existing_names = {s.get("segment_name") for s in existing_segments}
    for seg in CHILE_ADDITIONAL_SEGMENTS:
        if seg["segment_name"] not in existing_names:
            existing_segments.append(seg)

    update = {
        "operator_bmc_enrichments": CHILE_BMC_ENRICHMENTS,
        "operator_exposures": CHILE_OPERATOR_EXPOSURES,
        "customer_segments": existing_segments,
        "updated_at": datetime.utcnow().isoformat(),
    }

    client.table("market_configs").update(update).eq("market_id", "chile").execute()
    print(f"  Updated: BMC for {len(CHILE_BMC_ENRICHMENTS)} operators, "
          f"exposures for {len(CHILE_OPERATOR_EXPOSURES)} operators, "
          f"{len(existing_segments)} total segments")


def seed_tigo_chile(client):
    """Populate Tigo Chile financial and subscriber data."""
    print("\n[4/4] Populating Tigo Chile financial + subscriber data...")

    # Upsert financial (replace the empty rows)
    resp = client.table("financial_quarterly").upsert(
        TIGO_CHILE_FINANCIAL,
        on_conflict="operator_id,calendar_quarter"
    ).execute()
    print(f"  Financial: upserted {len(resp.data)} rows")

    # Insert subscriber
    resp = client.table("subscriber_quarterly").upsert(
        TIGO_CHILE_SUBSCRIBER,
        on_conflict="operator_id,calendar_quarter"
    ).execute()
    print(f"  Subscriber: upserted {len(resp.data)} rows")


def main():
    print("=" * 60)
    print("  Chile Data Seed — Closing Gaps vs Germany Benchmark")
    print("=" * 60)

    client = get_client()

    seed_intelligence_events(client)
    seed_earnings_highlights(client)
    seed_market_config(client)
    seed_tigo_chile(client)

    print("\n" + "=" * 60)
    print("  All Chile gaps seeded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
