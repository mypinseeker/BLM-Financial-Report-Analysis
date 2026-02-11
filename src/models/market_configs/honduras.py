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
