"""El Salvador telecom market configuration."""

from src.models.market_config import MarketConfig

EL_SALVADOR_CONFIG = MarketConfig(
    market_id="el_salvador",
    market_name="El Salvador",
    country="El Salvador",
    currency="USD",
    currency_symbol="$",
    regulatory_body="SIGET (Superintendencia General de Electricidad y Telecomunicaciones)",
    population_k=6500,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable unlimited social media plans",
                "Better rural coverage",
            ],
            "pain_points": [
                "High per-GB costs",
                "Coverage gaps in rural departments",
            ],
            "purchase_decision_factors": [
                "Price",
                "Data for social media",
                "Network coverage",
            ],
        },
        {
            "segment_name": "Consumer Postpaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Convergent bundles (mobile + home)",
                "Better device financing options",
            ],
            "pain_points": [
                "Limited postpaid plan options",
                "Contract rigidity",
            ],
            "purchase_decision_factors": [
                "Plan value",
                "Device subsidies",
                "Network quality",
            ],
        },
        {
            "segment_name": "Enterprise",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Cloud and connectivity solutions",
                "Cybersecurity services",
            ],
            "pain_points": [
                "Limited enterprise product portfolio",
                "High costs for dedicated lines",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price competitiveness",
                "Technical support",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_el_salvador": {
            "key_resources": ["HFC cable network", "4G mobile coverage", "Tigo Money mobile wallet"],
            "value_propositions": ["Convergent mobile+cable+TV", "Mobile money/Bitcoin integration"],
            "key_partners": ["Millicom group", "Ericsson"],
            "key_activities": ["Cable broadband expansion", "Fintech/Bitcoin integration", "Data monetization"],
        },
        "claro_sv": {
            "key_resources": ["Largest 4G mobile network", "Fiber broadband infrastructure"],
            "value_propositions": ["Best mobile coverage", "Enterprise solutions"],
            "key_partners": ["America Movil group"],
        },
        "digicel_sv": {
            "key_resources": ["Mobile network"],
            "value_propositions": ["Budget mobile plans"],
        },
    },

    operator_exposures={
        "tigo_el_salvador": [
            {
                "trigger_action": "Bitcoin legal tender creates operational complexity",
                "side_effect": "Currency volatility risk on Bitcoin-denominated transactions",
                "attack_vector": "Regulatory uncertainty around cryptocurrency telecom payments",
                "severity": "medium",
                "evidence": ["El Salvador Bitcoin law", "Chivo wallet integration requirements"],
            },
            {
                "trigger_action": "Claro leads in mobile market share and coverage",
                "side_effect": "Tigo positioned as #2 in mobile, relies on fixed for differentiation",
                "attack_vector": "Claro expanding fiber erodes Tigo's fixed broadband advantage",
                "severity": "medium",
                "evidence": ["Claro 82% 4G coverage vs Tigo 80%"],
            },
        ],
        "claro_sv": [
            {
                "trigger_action": "Tigo's cable+TV convergent advantage",
                "side_effect": "Claro lacks cable TV offering for bundling",
                "attack_vector": "Tigo bundles erode Claro mobile-only value",
                "severity": "medium",
                "evidence": ["Tigo cable TV market leader"],
            },
        ],
        "digicel_sv": [
            {
                "trigger_action": "Financial distress at group level",
                "side_effect": "Near-certain market exit or acquisition",
                "attack_vector": "Tigo and Claro absorb Digicel subscribers",
                "severity": "high",
                "evidence": ["Digicel Group debt restructuring", "Subscriber losses accelerating"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_el_salvador": {
            "controlled_vs_resale": "Fully owned mobile 4G + HFC cable network (550K homes). ~95% self-built.",
            "evolution_strategy": "4G LTE densification; cable DOCSIS 3.1 upgrade; fiber overlay in San Salvador; Bitcoin payment integration.",
            "consumer_impact": "Strong convergent bundle; cable broadband up to 200 Mbps; good 4G coverage; fintech innovation.",
            "b2b_impact": "Growing Tigo Business for SMEs; connectivity + fintech solutions; Bitcoin payment rails.",
            "cost_impact": "Cable efficient for broadband; compact geography aids deployment economics; Millicom procurement.",
            "org_culture": "Innovative (fintech/Bitcoin); Millicom standards; agile in compact market; digital-first approach.",
        },
        "claro_sv": {
            "controlled_vs_resale": "Own mobile 4G network + growing fiber broadband. ~92% self-built.",
            "evolution_strategy": "4G densification; fiber broadband expansion; mobile data growth.",
            "consumer_impact": "Best mobile coverage; growing fiber broadband; device financing; premium positioning.",
            "b2b_impact": "Enterprise solutions via America Movil; growing cloud/managed services.",
            "cost_impact": "America Movil procurement; efficient operations; fiber investment incremental.",
            "org_culture": "America Movil discipline; market leader confidence; results-driven.",
        },
        "digicel_sv": {
            "controlled_vs_resale": "Own mobile network, 35% 4G coverage. No fixed. Declining investment.",
            "evolution_strategy": "Exit/maintenance mode; no expansion; potential market exit.",
            "consumer_impact": "Budget pricing; poor network quality; declining relevance.",
            "b2b_impact": "None.",
            "cost_impact": "Minimal capex; network degradation.",
            "org_culture": "Survival mode; Digicel Group financial distress.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Claro (leader), Tigo, Digicel",
        "Dollarized economy simplifies pricing",
        "Claro leads mobile market share",
        "Tigo strong in cable and broadband",
        "Compact geography aids coverage deployment",
    ],

    pest_context={
        "political": [
            "Bitcoin as legal tender creating fintech opportunities",
            "Government security improvements boosting investment",
            "SIGET regulatory framework",
        ],
        "economic": [
            "Dollarized economy (USD), GDP growth ~2.8%",
            "Remittances significant (>20% of GDP)",
            "Growing tech sector in San Salvador",
        ],
        "social": [
            "Young demographic driving mobile usage",
            "Urbanized population concentrated in San Salvador metro",
            "Rising digital payment adoption",
        ],
        "technological": [
            "4G LTE widespread in urban areas",
            "Cable broadband dominant for fixed",
            "Mobile wallet/fintech growing rapidly",
        ],
    },
)
