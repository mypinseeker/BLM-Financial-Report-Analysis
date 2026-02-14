"""Honduras telecom market configuration."""

from src.models.market_config import MarketConfig

HONDURAS_CONFIG = MarketConfig(
    market_id="honduras",
    market_name="Honduras",
    country="Honduras",
    currency="HNL",
    currency_symbol="L",
    regulatory_body="CONATEL",
    population_k=10400,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data bundles for low income",
                "Rural connectivity",
            ],
            "pain_points": [
                "Limited coverage outside major cities",
                "Expensive data relative to income",
            ],
            "purchase_decision_factors": [
                "Price",
                "Coverage",
                "Social media access",
            ],
        },
        {
            "segment_name": "Consumer Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster mobile broadband",
                "Home internet bundles",
            ],
            "pain_points": [
                "Network quality issues",
                "Limited plan variety",
            ],
            "purchase_decision_factors": [
                "Speed",
                "Data volume",
                "Device offers",
            ],
        },
        {
            "segment_name": "Enterprise",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Enterprise-grade connectivity",
                "Managed IT services",
            ],
            "pain_points": [
                "Limited B2B solutions",
                "Unreliable infrastructure",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price",
                "Support quality",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_honduras": {
            "key_resources": ["Largest HFC cable network", "Widest 4G mobile coverage", "Tigo Money mobile wallet"],
            "value_propositions": ["Convergent mobile+cable+TV bundles", "Mobile financial services via Tigo Money"],
            "key_partners": ["Millicom group shared services", "Ericsson network infrastructure"],
            "key_activities": ["Cable broadband expansion to secondary cities", "Mobile data monetization", "Financial inclusion via Tigo Money"],
        },
        "claro_hn": {
            "key_resources": ["Strong mobile network", "America Movil group capabilities"],
            "value_propositions": ["Reliable mobile service", "Device financing options"],
            "key_partners": ["America Movil group procurement"],
        },
        "digicel_hn": {
            "key_resources": ["Low-cost mobile network"],
            "value_propositions": ["Budget mobile plans"],
            "key_activities": ["Market share defense on price"],
        },
    },

    operator_exposures={
        "tigo_honduras": [
            {
                "trigger_action": "Political and economic instability affecting investment climate",
                "side_effect": "Currency depreciation increasing equipment costs, potential regulatory uncertainty",
                "attack_vector": "Economic downturn reduces consumer spending on telecom services",
                "severity": "medium",
                "evidence": ["Honduras political uncertainty", "HNL depreciation trend"],
            },
            {
                "trigger_action": "Dependence on prepaid revenue in low-income market",
                "side_effect": "Limited ARPU growth potential constrained by purchasing power",
                "attack_vector": "Economic pressure squeezes consumer telecom spending",
                "severity": "medium",
                "evidence": ["~85% prepaid market", "Low per-capita income"],
            },
        ],
        "claro_hn": [
            {
                "trigger_action": "Tigo's cable+mobile bundle advantage",
                "side_effect": "Inability to compete on convergent offerings",
                "attack_vector": "Tigo bundles erode Claro mobile-only value proposition",
                "severity": "high",
                "evidence": ["Claro lacks fixed broadband infrastructure"],
            },
        ],
        "digicel_hn": [
            {
                "trigger_action": "Financial distress at group level",
                "side_effect": "Reduced investment and potential market exit",
                "attack_vector": "Tigo and Claro absorb Digicel subscribers on exit",
                "severity": "high",
                "evidence": ["Digicel Group debt restructuring", "Declining subscriber count"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_honduras": {
            "controlled_vs_resale": "Fully owned mobile 4G network + HFC cable network (900K homes passed). ~95% self-built infrastructure.",
            "evolution_strategy": "4G LTE coverage expansion to 80%+ population; HFC upgrade to DOCSIS 3.1; fiber overlay in Tegucigalpa and San Pedro Sula.",
            "consumer_impact": "Best convergent offering (mobile+broadband+TV); cable broadband up to 200 Mbps; reliable 4G in urban/semi-urban areas.",
            "b2b_impact": "Growing Tigo Business segment for SMEs; connectivity solutions for maquila sector; limited enterprise cloud capability.",
            "cost_impact": "Cable network efficient for broadband delivery; moderate mobile capex; Millicom group procurement benefits.",
            "org_culture": "Market leader confidence; strong local management; Millicom operational standards; community engagement via Tigo Money.",
        },
        "claro_hn": {
            "controlled_vs_resale": "Own mobile network (4G LTE). Limited fixed infrastructure — fiber in select urban areas. ~88% own mobile network.",
            "evolution_strategy": "4G LTE expansion; selective fiber deployment; spectrum efficiency improvements.",
            "consumer_impact": "Good mobile coverage and quality; competitive pricing; limited fixed broadband reach constrains convergence.",
            "b2b_impact": "Enterprise solutions via America Movil platform; limited by lack of fixed infrastructure.",
            "cost_impact": "America Movil procurement advantages; efficient mobile operations; fiber buildout is incremental.",
            "org_culture": "America Movil competitive culture; results-oriented; focused on mobile market share.",
        },
        "digicel_hn": {
            "controlled_vs_resale": "Own mobile network with limited 4G coverage (~40% pop). No fixed infrastructure. ~100% own mobile but limited.",
            "evolution_strategy": "Minimal network investment; maintaining existing coverage; no expansion plans amid financial difficulties.",
            "consumer_impact": "Budget positioning; poor network quality; coverage gaps; declining relevance.",
            "b2b_impact": "No enterprise presence; purely consumer mobile.",
            "cost_impact": "Lowest capex in market; network degradation risk; group-level financial constraints limiting investment.",
            "org_culture": "Survival mode; Digicel Group restructuring pressure; high staff turnover; uncertain future.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Tigo (leader), Claro, Digicel",
        "Tigo leads mobile and cable broadband",
        "Heavily prepaid-driven market",
        "Digicel positioned as value alternative",
        "Growing demand for mobile data services",
    ],

    pest_context={
        "political": [
            "CONATEL regulating spectrum allocation",
            "Government push for rural connectivity",
            "Political instability affecting investment climate",
        ],
        "economic": [
            "GDP growth ~3.2%",
            "Large remittance-dependent economy",
            "Significant informal economy",
        ],
        "social": [
            "Young population with rising smartphone adoption",
            "High urbanization driving broadband demand",
            "Social media as primary communication channel",
        ],
        "technological": [
            "4G LTE rollout ongoing",
            "Cable broadband expanding in urban areas",
            "Mobile money services emerging",
        ],
    },
)
