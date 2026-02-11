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
