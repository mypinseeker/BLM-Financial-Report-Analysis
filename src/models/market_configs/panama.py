"""Panama telecom market configuration."""

from src.models.market_config import MarketConfig

PANAMA_CONFIG = MarketConfig(
    market_id="panama",
    market_name="Panama",
    country="Panama",
    currency="USD",
    currency_symbol="$",
    regulatory_body="ASEP (Autoridad Nacional de los Servicios Publicos)",
    population_k=4400,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better data value for money",
                "Coverage outside Panama City corridor",
            ],
            "pain_points": [
                "Limited competitive options",
                "Data expiry on prepaid bundles",
            ],
            "purchase_decision_factors": [
                "Price",
                "Data allowance",
                "Coverage",
            ],
        },
        {
            "segment_name": "Consumer Postpaid & Premium",
            "segment_type": "consumer",
            "unmet_needs": [
                "High-speed broadband for remote work",
                "Premium convergent bundles",
            ],
            "pain_points": [
                "Limited fixed broadband options",
                "High prices for premium tiers",
            ],
            "purchase_decision_factors": [
                "Speed",
                "Reliability",
                "Bundle options",
            ],
        },
        {
            "segment_name": "Enterprise & Canal Zone",
            "segment_type": "enterprise",
            "unmet_needs": [
                "International connectivity for logistics/shipping",
                "Data center and cloud services",
            ],
            "pain_points": [
                "Limited enterprise-grade solutions",
                "High cost of international connectivity",
            ],
            "purchase_decision_factors": [
                "International connectivity",
                "Reliability",
                "Price",
            ],
        },
    ],

    competitive_landscape_notes=[
        "3-player market: Claro (leader), Tigo, Digicel",
        "Dollarized economy (USD) like El Salvador",
        "Claro leads mobile market",
        "Panama Canal zone drives enterprise connectivity demand",
        "Relatively high GDP per capita for Central America",
    ],

    pest_context={
        "political": [
            "ASEP regulatory framework",
            "Government infrastructure investment programs",
            "Panama as regional financial hub",
        ],
        "economic": [
            "GDP growth ~5%, driven by Canal and services",
            "Dollarized economy provides stability",
            "Strong banking and logistics sectors",
        ],
        "social": [
            "Small but affluent population",
            "High smartphone penetration",
            "Growing demand for digital services",
        ],
        "technological": [
            "4G LTE well-deployed in urban areas",
            "Submarine cable hub for Americas",
            "Growing data center market",
        ],
    },
)
