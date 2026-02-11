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
