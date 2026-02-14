"""Nicaragua telecom market configuration."""

from src.models.market_config import MarketConfig

NICARAGUA_CONFIG = MarketConfig(
    market_id="nicaragua",
    market_name="Nicaragua",
    country="Nicaragua",
    currency="NIO",
    currency_symbol="C$",
    regulatory_body="TELCOR (Instituto Nicaraguense de Telecomunicaciones)",
    population_k=6900,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data access",
                "Coverage beyond Managua",
            ],
            "pain_points": [
                "Very limited rural connectivity",
                "Expensive data relative to income",
            ],
            "purchase_decision_factors": [
                "Price",
                "Coverage",
                "Social media bundles",
            ],
        },
        {
            "segment_name": "Consumer Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Reliable home broadband",
                "Better mobile speeds",
            ],
            "pain_points": [
                "Slow and unreliable internet",
                "Limited plan options",
            ],
            "purchase_decision_factors": [
                "Price",
                "Speed",
                "Reliability",
            ],
        },
        {
            "segment_name": "Enterprise",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Business-grade connectivity",
                "Basic cloud services",
            ],
            "pain_points": [
                "Very limited enterprise solutions",
                "Infrastructure unreliability",
            ],
            "purchase_decision_factors": [
                "Availability",
                "Price",
                "Reliability",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_nicaragua": {
            "key_resources": ["Largest mobile 4G network", "HFC cable network in Managua"],
            "value_propositions": ["Mobile + cable bundles", "Tigo Money mobile wallet"],
            "key_partners": ["Millicom group"],
            "key_activities": ["4G coverage expansion", "Cable broadband growth", "Mobile financial services"],
        },
        "claro_ni": {
            "key_resources": ["Mobile network", "America Movil group capabilities"],
            "value_propositions": ["Competitive mobile pricing"],
            "key_partners": ["America Movil group"],
        },
    },

    operator_exposures={
        "tigo_nicaragua": [
            {
                "trigger_action": "Political instability and sanctions environment",
                "side_effect": "Investment risk and potential operational restrictions",
                "attack_vector": "Regulatory uncertainty; sanctions affecting business environment",
                "severity": "high",
                "evidence": ["Nicaragua political situation", "International sanctions"],
            },
            {
                "trigger_action": "Smallest market in Millicom portfolio limits strategic priority",
                "side_effect": "Lower investment priority relative to Guatemala, Colombia",
                "attack_vector": "Underinvestment risk as Millicom optimizes group capital allocation",
                "severity": "medium",
                "evidence": ["Nicaragua smallest LATAM market by revenue"],
            },
        ],
        "claro_ni": [
            {
                "trigger_action": "Tigo's cable+mobile convergent advantage",
                "side_effect": "Inability to compete on fixed broadband bundling",
                "attack_vector": "Tigo bundles mobile+cable in Managua",
                "severity": "medium",
                "evidence": ["Claro lacks cable TV infrastructure"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_nicaragua": {
            "controlled_vs_resale": "Own mobile 4G + HFC cable network (350K homes in Managua). ~93% self-built.",
            "evolution_strategy": "4G LTE coverage expansion beyond Managua; cable broadband upgrade; selective fiber deployment.",
            "consumer_impact": "Best mobile coverage (60% pop); cable broadband in Managua; Tigo Money for financial inclusion.",
            "b2b_impact": "Limited enterprise segment; basic connectivity for SMEs; Tigo Business nascent.",
            "cost_impact": "Moderate capex; challenging political environment; Millicom procurement benefits; small market scale.",
            "org_culture": "Resilient operations in challenging environment; Millicom standards; community engagement.",
        },
        "claro_ni": {
            "controlled_vs_resale": "Own mobile network with 52% 4G coverage. Limited fixed. ~88% own mobile.",
            "evolution_strategy": "Selective 4G expansion; fiber in Managua; efficiency-focused.",
            "consumer_impact": "Good mobile coverage; competitive pricing; limited broadband offering.",
            "b2b_impact": "Basic enterprise solutions via America Movil platform.",
            "cost_impact": "America Movil procurement; efficient mobile operations; limited infrastructure investment.",
            "org_culture": "America Movil discipline; cautious investment given political risk.",
        },
    },

    competitive_landscape_notes=[
        "2-player mobile market: Tigo (leader), Claro",
        "Tigo dominates with ~55% mobile share",
        "Smallest addressable market in Millicom LATAM portfolio",
        "Limited fixed broadband infrastructure",
        "Highly prepaid-driven market",
    ],

    pest_context={
        "political": [
            "TELCOR regulating telecommunications",
            "Political instability affecting foreign investment",
            "International sanctions impacting business environment",
        ],
        "economic": [
            "GDP growth ~3.5%, lowest GDP per capita in Central America",
            "Remittances significant economic driver",
            "Limited foreign investment inflow",
        ],
        "social": [
            "Young population driving mobile adoption",
            "Rural population significant (~40%)",
            "Growing digital literacy in urban areas",
        ],
        "technological": [
            "4G LTE concentrated in Managua",
            "Limited fixed broadband penetration",
            "Mobile as primary internet access method",
        ],
    },
)
