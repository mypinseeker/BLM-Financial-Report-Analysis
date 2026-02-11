"""Chile telecom market configuration."""

from src.models.market_config import MarketConfig

CHILE_CONFIG = MarketConfig(
    market_id="chile",
    market_name="Chile",
    country="Chile",
    currency="CLP",
    currency_symbol="$",
    regulatory_body="SUBTEL (Subsecretaria de Telecomunicaciones)",
    population_k=19500,

    customer_segments=[
        {
            "segment_name": "Consumer Postpaid Premium",
            "segment_type": "consumer",
            "unmet_needs": [
                "5G coverage and experiences",
                "Premium convergent bundles (fiber+mobile+streaming)",
            ],
            "pain_points": [
                "5G deployment slower than expected",
                "Complex multi-play pricing",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "5G availability",
                "Bundle value",
                "Brand perception",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better value mobile plans",
                "Reliable home broadband",
            ],
            "pain_points": [
                "Price competition driving confusion",
                "Service quality inconsistency",
            ],
            "purchase_decision_factors": [
                "Price-performance ratio",
                "Data volume",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive",
            "segment_type": "consumer",
            "unmet_needs": [
                "Ultra-low-cost data plans",
                "No-contract flexibility",
            ],
            "pain_points": [
                "WOM disruption raising expectations",
                "Data caps at budget tier",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "No-contract options",
            ],
        },
        {
            "segment_name": "Enterprise Large",
            "segment_type": "enterprise",
            "unmet_needs": [
                "SD-WAN and multi-cloud solutions",
                "Private 5G for mining and logistics",
            ],
            "pain_points": [
                "Limited 5G enterprise solutions",
                "High cost of dedicated circuits",
            ],
            "purchase_decision_factors": [
                "Network reliability",
                "SLA guarantees",
                "Innovation capability",
            ],
        },
        {
            "segment_name": "Enterprise SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Simple all-in-one business solutions",
                "Affordable cloud hosting",
            ],
            "pain_points": [
                "Complex B2B pricing",
                "Slow provisioning",
            ],
            "purchase_decision_factors": [
                "Price",
                "Simplicity",
                "Reliability",
            ],
        },
    ],

    competitive_landscape_notes=[
        "5-player market: Entel, Movistar, Claro, WOM, Tigo (smallest)",
        "WOM disrupted market since 2015 with aggressive pricing",
        "Entel leads in premium mobile, Movistar in convergent",
        "Chile most competitive LATAM telecom market",
        "Tigo has smallest market share, partnership/MVNO model",
        "5G launched by Entel, WOM, Movistar",
    ],

    pest_context={
        "political": [
            "SUBTEL active in spectrum allocation and competition",
            "New constitution process affecting regulatory framework",
            "Government pushing 5G deployment",
        ],
        "economic": [
            "GDP growth ~2.5%, highest GDP per capita in LATAM",
            "Peso volatility affecting equipment costs",
            "Mature consumer economy",
        ],
        "social": [
            "High smartphone penetration (~85%)",
            "Strong streaming and digital services adoption",
            "Demanding consumers with high service expectations",
        ],
        "technological": [
            "5G commercial launch in major cities",
            "Fiber broadband expanding rapidly",
            "Most advanced telecom market in LATAM",
            "High 4G penetration (~90%)",
        ],
    },
)
