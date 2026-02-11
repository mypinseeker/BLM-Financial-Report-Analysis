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
