"""Paraguay telecom market configuration."""

from src.models.market_config import MarketConfig

PARAGUAY_CONFIG = MarketConfig(
    market_id="paraguay",
    market_name="Paraguay",
    country="Paraguay",
    currency="PYG",
    currency_symbol="Gs",
    regulatory_body="CONATEL (Comision Nacional de Telecomunicaciones)",
    population_k=7400,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data bundles",
                "Better rural coverage",
            ],
            "pain_points": [
                "Coverage gaps outside Asuncion",
                "Low data allowances on prepaid",
            ],
            "purchase_decision_factors": [
                "Price",
                "Data volume",
                "Coverage",
            ],
        },
        {
            "segment_name": "Consumer Urban Postpaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Convergent mobile + broadband bundles",
                "Better speeds",
            ],
            "pain_points": [
                "Limited fixed broadband availability",
                "Slow internet speeds",
            ],
            "purchase_decision_factors": [
                "Speed",
                "Bundle options",
                "Price",
            ],
        },
        {
            "segment_name": "Enterprise",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Enterprise-grade connectivity",
                "Cloud and managed services",
            ],
            "pain_points": [
                "Limited enterprise product catalog",
                "Reliability issues",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price",
                "Technical support",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_paraguay": {
            "key_resources": ["Largest HFC cable network", "Widest 4G mobile coverage", "Tigo Money mobile wallet"],
            "value_propositions": ["Convergent mobile+cable+TV bundles", "Mobile financial services"],
            "key_partners": ["Millicom group shared services", "Ericsson"],
            "key_activities": ["Cable broadband expansion", "Data monetization", "Financial inclusion"],
        },
        "claro_py": {
            "key_resources": ["Strong mobile network", "America Movil group capabilities"],
            "value_propositions": ["Reliable mobile service", "Device financing"],
            "key_partners": ["America Movil group procurement"],
        },
        "personal_py": {
            "key_resources": ["Telecom Argentina network platform"],
            "value_propositions": ["Value mobile plans"],
        },
    },

    operator_exposures={
        "tigo_paraguay": [
            {
                "trigger_action": "Dependence on prepaid in low-income market",
                "side_effect": "Limited ARPU growth potential",
                "attack_vector": "Price competition from Claro targets Tigo's prepaid base",
                "severity": "medium",
                "evidence": ["~85% prepaid market", "Low GDP per capita"],
            },
            {
                "trigger_action": "Cable network upgrade requirement for DOCSIS 3.1",
                "side_effect": "Capex pressure for broadband competitiveness",
                "attack_vector": "Fiber entrants could bypass aging cable",
                "severity": "medium",
                "evidence": ["HFC network serves 600K homes"],
            },
        ],
        "claro_py": [
            {
                "trigger_action": "Tigo cable+mobile convergent advantage",
                "side_effect": "Inability to offer fixed broadband bundles",
                "attack_vector": "Tigo bundles mobile+cable+TV",
                "severity": "high",
                "evidence": ["Claro lacks fixed broadband infrastructure"],
            },
        ],
        "personal_py": [
            {
                "trigger_action": "Declining subscriber base and parent company challenges",
                "side_effect": "Underinvestment and potential market exit",
                "attack_vector": "Telecom Argentina financial difficulties limiting subsidiary investment",
                "severity": "high",
                "evidence": ["Negative growth trend", "Telecom Argentina restructuring"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_paraguay": {
            "controlled_vs_resale": "Fully owned mobile 4G network + HFC cable network (600K homes passed). ~95% self-built.",
            "evolution_strategy": "4G LTE densification; HFC DOCSIS 3.1 upgrade; fiber overlay in Asuncion.",
            "consumer_impact": "Best convergent bundle in market; cable broadband up to 200 Mbps; strong 4G in urban areas.",
            "b2b_impact": "Growing Tigo Business for SMEs; connectivity solutions; limited enterprise cloud.",
            "cost_impact": "Cable network efficient for broadband; moderate mobile capex; Millicom procurement benefits.",
            "org_culture": "Market leader confidence; Millicom standards; focus on digital inclusion and Tigo Money.",
        },
        "claro_py": {
            "controlled_vs_resale": "Own mobile network with 4G LTE. Limited fixed infrastructure. ~90% own mobile.",
            "evolution_strategy": "4G expansion; selective fiber deployment; spectrum efficiency.",
            "consumer_impact": "Good mobile coverage; competitive pricing; no fixed broadband offering.",
            "b2b_impact": "Enterprise solutions via America Movil; limited by lack of fixed infrastructure.",
            "cost_impact": "America Movil procurement advantages; efficient mobile operations.",
            "org_culture": "America Movil competitive discipline; results-focused.",
        },
        "personal_py": {
            "controlled_vs_resale": "Own mobile network with limited 4G (~45% pop). No fixed. ~100% own mobile but declining.",
            "evolution_strategy": "Maintenance mode; limited expansion; uncertain commitment.",
            "consumer_impact": "Declining quality perception; competitive pricing; coverage gaps.",
            "b2b_impact": "Minimal enterprise presence.",
            "cost_impact": "Low capex constraining quality; parent company financial pressure.",
            "org_culture": "Defensive; Telecom Argentina constraints; uncertain future.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Tigo (leader), Claro, Personal",
        "Tigo dominates mobile with ~50% share",
        "Tigo also leads cable TV and broadband",
        "Personal (Telecom Argentina) as third player",
        "Growing smartphone and data adoption",
    ],

    pest_context={
        "political": [
            "CONATEL regulatory oversight",
            "Government push for digital government services",
            "Relatively stable regulatory environment",
        ],
        "economic": [
            "GDP growth ~4%, agriculture-driven economy",
            "Landlocked country with trade dependencies",
            "Growing urbanization driving telecom demand",
        ],
        "social": [
            "Young population (median age ~26)",
            "High mobile penetration relative to region",
            "Bilingual (Spanish/Guarani) market",
        ],
        "technological": [
            "4G LTE expanding from urban centers",
            "Cable broadband via Tigo HFC network",
            "Mobile payments growing via Tigo Money",
        ],
    },
)
