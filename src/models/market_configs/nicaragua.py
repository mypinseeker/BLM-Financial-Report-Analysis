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
