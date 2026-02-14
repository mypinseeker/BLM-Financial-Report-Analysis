"""Guatemala telecom market configuration."""

from src.models.market_config import MarketConfig

GUATEMALA_CONFIG = MarketConfig(
    market_id="guatemala",
    market_name="Guatemala",
    country="Guatemala",
    currency="GTQ",
    currency_symbol="Q",
    regulatory_body="SIT (Superintendencia de Telecomunicaciones)",
    population_k=17600,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable mobile data in rural areas",
                "Spanish + indigenous language customer support",
            ],
            "pain_points": [
                "Limited rural coverage",
                "Complex recharge mechanisms",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Coverage in home area",
                "Social media bundles",
            ],
        },
        {
            "segment_name": "Consumer Postpaid Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster 4G/LTE speeds",
                "Convergent home+mobile bundles",
            ],
            "pain_points": [
                "High prices relative to income",
                "Network congestion in Guatemala City",
            ],
            "purchase_decision_factors": [
                "Data allowance",
                "Network quality",
                "Device financing",
            ],
        },
        {
            "segment_name": "Enterprise & SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Cloud connectivity solutions",
                "Reliable business broadband",
            ],
            "pain_points": [
                "Limited B2B product portfolio",
                "Slow provisioning",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "SLA guarantees",
                "Price",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_guatemala": {
            "key_resources": ["Largest HFC cable network in Guatemala", "Widest 4G mobile coverage"],
            "value_propositions": ["Convergent mobile+cable+TV bundles", "Tigo Money mobile wallet"],
            "key_partners": ["Millicom group shared services", "Ericsson network infrastructure"],
            "key_activities": ["Cable broadband expansion", "Mobile data monetization"],
        },
        "claro_gt": {
            "key_resources": ["Strong postpaid subscriber base", "America Movil group capabilities"],
            "value_propositions": ["Premium device portfolio", "Enterprise solutions"],
            "key_partners": ["America Movil group procurement"],
        },
        "movistar_gt": {
            "key_resources": ["Telefonica Group technology stack"],
            "value_propositions": ["Value-oriented mobile plans"],
            "key_activities": ["Market share defense"],
        },
    },

    operator_exposures={
        "tigo_guatemala": [
            {
                "trigger_action": "Dependence on prepaid revenue in price-sensitive market",
                "side_effect": "Vulnerable to aggressive pricing from competitors",
                "attack_vector": "Claro or new MVNO could undercut Tigo on prepaid pricing",
                "severity": "medium",
                "evidence": ["~80% prepaid subscriber base", "Prepaid ARPU under pressure"],
            },
            {
                "trigger_action": "Cable network aging requires DOCSIS upgrade investment",
                "side_effect": "Capex pressure to maintain broadband competitiveness",
                "attack_vector": "Fiber entrants could bypass cable with FTTH offerings",
                "severity": "medium",
                "evidence": ["HFC network serves 1.2M homes", "Fiber homepass still small at 800K"],
            },
        ],
        "claro_gt": [
            {
                "trigger_action": "Tigo's dominance in cable broadband creates convergent advantage",
                "side_effect": "Claro lacks fixed-line bundling capability",
                "attack_vector": "Tigo bundles mobile+cable+TV at attractive price points",
                "severity": "high",
                "evidence": ["Claro fiber coverage limited", "No cable TV offering"],
            },
        ],
        "movistar_gt": [
            {
                "trigger_action": "Declining subscriber base and revenue",
                "side_effect": "Potential market exit or reduced investment",
                "attack_vector": "Telefonica divesting non-core LATAM markets",
                "severity": "high",
                "evidence": ["Negative growth for 8 consecutive quarters"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_guatemala": {
            "controlled_vs_resale": "Fully owned mobile 4G network + largest HFC cable network in Guatemala. ~95% self-built infrastructure.",
            "evolution_strategy": "4G LTE densification to reach 85% population coverage; HFC upgrade to DOCSIS 3.1; parallel FTTH deployment in Guatemala City and secondary cities.",
            "consumer_impact": "Strongest convergent bundle (mobile+broadband+TV) in market; cable broadband up to 300 Mbps; reliable 4G in urban areas; expanding rural coverage.",
            "b2b_impact": "Growing enterprise segment with cloud connectivity; Tigo Business targeting SMEs; limited private network capability vs developed markets.",
            "cost_impact": "Cable network provides cost-efficient broadband delivery; 4G mobile capex moderate; Millicom group procurement reduces equipment costs.",
            "org_culture": "Market-leading confidence; strong commercial execution; Millicom operational standards; focus on digital inclusion and financial services (Tigo Money).",
        },
        "claro_gt": {
            "controlled_vs_resale": "Own mobile network with broad 4G coverage. Fiber broadband in limited areas. ~90% self-built.",
            "evolution_strategy": "4G LTE expansion; fiber broadband build in Guatemala City; spectrum efficiency improvements.",
            "consumer_impact": "Strong postpaid and device financing; good urban coverage; limited fixed broadband reach.",
            "b2b_impact": "Enterprise solutions via America Movil platform; data center capabilities; growing cloud services.",
            "cost_impact": "America Movil group procurement advantages; efficient mobile operations; fiber buildout requires incremental capex.",
            "org_culture": "America Movil competitive culture; results-driven management; strong commercial discipline.",
        },
        "movistar_gt": {
            "controlled_vs_resale": "Own mobile network with declining coverage investment. ~85% own-network.",
            "evolution_strategy": "Maintenance-mode network investment; selective 4G deployment; uncertain long-term commitment.",
            "consumer_impact": "Declining network quality perception; competitive pricing but coverage gaps; losing relevance in market.",
            "b2b_impact": "Minimal enterprise presence; focusing on consumer segment survival.",
            "cost_impact": "Reduced capex constraining network quality; potential for further investment cuts if decline continues.",
            "org_culture": "Defensive posture; Telefonica Group LATAM rationalization pressure; uncertain market commitment.",
        },
    },

    competitive_landscape_notes=[
        "3-player mobile market: Tigo (leader), Claro, Movistar",
        "Tigo dominates with ~50% mobile market share",
        "Prepaid-dominant market (~80% of connections)",
        "Growing HFC cable TV and broadband from Tigo",
        "Claro strong in postpaid and enterprise segments",
    ],

    pest_context={
        "political": [
            "Stable regulatory environment under SIT",
            "Government digital inclusion programs",
            "Free-market telecom policies",
        ],
        "economic": [
            "GDP growth ~3.5%, largest Central American economy",
            "Significant remittance economy (15% of GDP)",
            "Growing middle class driving smartphone adoption",
        ],
        "social": [
            "Young population (median age ~22)",
            "High mobile penetration, low fixed broadband",
            "Social media and messaging apps driving data usage",
        ],
        "technological": [
            "4G LTE deployment expanding",
            "Cable/HFC broadband growing in urban areas",
            "Mobile money services gaining traction",
        ],
    },
)
