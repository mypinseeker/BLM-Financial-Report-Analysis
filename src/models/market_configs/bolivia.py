"""Bolivia telecom market configuration."""

from src.models.market_config import MarketConfig

BOLIVIA_CONFIG = MarketConfig(
    market_id="bolivia",
    market_name="Bolivia",
    country="Bolivia",
    currency="BOB",
    currency_symbol="Bs",
    regulatory_body="ATT (Autoridad de Regulacion y Fiscalizacion de Telecomunicaciones)",
    population_k=12200,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data in rural/highland areas",
                "Indigenous language support",
            ],
            "pain_points": [
                "Very limited rural coverage",
                "High cost per GB relative to income",
            ],
            "purchase_decision_factors": [
                "Price",
                "Coverage in home region",
                "Recharge availability",
            ],
        },
        {
            "segment_name": "Consumer Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster mobile data speeds",
                "Home broadband options",
            ],
            "pain_points": [
                "Slow data speeds",
                "Limited postpaid offerings",
            ],
            "purchase_decision_factors": [
                "Data volume",
                "Price",
                "Network quality",
            ],
        },
        {
            "segment_name": "Enterprise",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Reliable business connectivity",
                "Cloud services",
            ],
            "pain_points": [
                "Limited B2B solutions",
                "Infrastructure limitations",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price",
                "Coverage",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_bolivia": {
            "key_resources": ["Largest cable/HFC network", "Leading mobile 4G coverage", "Tigo Money"],
            "value_propositions": ["Convergent mobile+cable+TV", "Mobile financial services in underbanked market"],
            "key_partners": ["Millicom group shared services", "Ericsson"],
            "key_activities": ["Cable broadband expansion", "4G densification", "Financial inclusion"],
        },
        "entel_bo": {
            "key_resources": ["State-owned infrastructure", "Government backing and rural mandate", "Fiber backbone"],
            "value_propositions": ["Affordable pricing", "Widest rural coverage"],
            "key_activities": ["Rural connectivity mandate", "Government digitalization backbone"],
        },
        "viva_bo": {
            "key_resources": ["Mobile network"],
            "value_propositions": ["Budget mobile plans"],
        },
    },

    operator_exposures={
        "tigo_bolivia": [
            {
                "trigger_action": "Government favoritism toward state-owned Entel",
                "side_effect": "Regulatory asymmetry and spectrum allocation disadvantage",
                "attack_vector": "Entel receives government support and favorable spectrum terms",
                "severity": "high",
                "evidence": ["Entel state-owned with government backing", "ATT regulatory alignment with state interests"],
            },
            {
                "trigger_action": "Challenging geography (Andes + Amazon) limits rural coverage economics",
                "side_effect": "High per-site deployment costs in mountainous terrain",
                "attack_vector": "Entel with government subsidies can deploy in unprofitable rural areas",
                "severity": "medium",
                "evidence": ["Bolivia's extreme geography", "Rural coverage only ~40%"],
            },
        ],
        "entel_bo": [
            {
                "trigger_action": "State-owned inefficiency and political interference",
                "side_effect": "Slower innovation and service quality gaps",
                "attack_vector": "Tigo offers superior digital experience and customer service",
                "severity": "medium",
                "evidence": ["Government-appointed management", "Bureaucratic processes"],
            },
        ],
        "viva_bo": [
            {
                "trigger_action": "Third-player squeeze between Tigo and state-owned Entel",
                "side_effect": "Declining subscribers and revenue",
                "attack_vector": "Both Tigo and Entel outspend Viva on network and marketing",
                "severity": "high",
                "evidence": ["Negative growth trajectory", "Limited investment capacity"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_bolivia": {
            "controlled_vs_resale": "Fully owned mobile 4G + HFC cable network (450K homes). ~93% self-built.",
            "evolution_strategy": "4G LTE expansion to secondary cities; fiber deployment in Santa Cruz and La Paz; HFC DOCSIS 3.1.",
            "consumer_impact": "Best convergent bundle (mobile+cable+TV); broadband up to 150 Mbps; leading 4G coverage.",
            "b2b_impact": "Growing enterprise segment; Tigo Business for SMEs; limited cloud/data center.",
            "cost_impact": "Cable network efficient; mobile deployment expensive due to terrain; Millicom procurement.",
            "org_culture": "Market leader; Millicom standards; Tigo Money driving financial inclusion; challenging regulatory environment.",
        },
        "entel_bo": {
            "controlled_vs_resale": "State-owned mobile + fixed network. Fiber backbone. ~100% own-network.",
            "evolution_strategy": "Government-funded rural deployment; fiber expansion; 4G coverage improvement.",
            "consumer_impact": "Widest coverage including rural; affordable pricing; slower speeds vs Tigo.",
            "b2b_impact": "Government contracts; public sector connectivity; limited commercial enterprise.",
            "cost_impact": "Government-funded infrastructure; higher per-subscriber cost due to rural mandate.",
            "org_culture": "State enterprise; public service mandate; slow innovation; stable employment.",
        },
        "viva_bo": {
            "controlled_vs_resale": "Own mobile network with limited 4G (~38% pop). No fixed. ~100% own mobile.",
            "evolution_strategy": "Maintenance mode; minimal investment; uncertain future.",
            "consumer_impact": "Budget positioning; declining quality; limited 4G coverage.",
            "b2b_impact": "No enterprise presence.",
            "cost_impact": "Minimal capex; network degradation risk.",
            "org_culture": "Survival mode; constrained resources; uncertain strategic direction.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Tigo (leader), Entel (state-owned), Viva",
        "Tigo leads mobile market share (~45%)",
        "Entel has government backing and rural mandate",
        "Viva as value-oriented third player",
        "Challenging geography (Andes + Amazon) limits coverage",
    ],

    pest_context={
        "political": [
            "ATT telecom regulation",
            "State-owned Entel as competitor and policy tool",
            "Government focus on rural connectivity",
        ],
        "economic": [
            "GDP growth ~3%, resource-dependent economy",
            "Low GDP per capita limits ARPU potential",
            "Informal economy significant portion of GDP",
        ],
        "social": [
            "Diverse indigenous population",
            "Rapid urbanization to La Paz, Santa Cruz, Cochabamba",
            "Growing youth smartphone adoption",
        ],
        "technological": [
            "4G LTE deployment concentrated in cities",
            "Challenging terrain for network deployment",
            "Mobile money growing as banking alternative",
        ],
    },
)
