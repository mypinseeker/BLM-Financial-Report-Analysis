"""Guatemala telecom market configuration."""

from src.models.market_config import MarketConfig

GUATEMALA_CONFIG = MarketConfig(
    market_id="guatemala",
    market_name="Guatemala",
    country="Guatemala",
    currency="GTQ",
    currency_symbol="Q",
    regulatory_body="SIT (Superintendencia de Telecomunicaciones)",
    population_k=17600,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable mobile data in rural areas",
                "Spanish + indigenous language customer support",
            ],
            "pain_points": [
                "Limited rural coverage",
                "Complex recharge mechanisms",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Coverage in home area",
                "Social media bundles",
            ],
        },
        {
            "segment_name": "Consumer Postpaid Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster 4G/LTE speeds",
                "Convergent home+mobile bundles",
            ],
            "pain_points": [
                "High prices relative to income",
                "Network congestion in Guatemala City",
            ],
            "purchase_decision_factors": [
                "Data allowance",
                "Network quality",
                "Device financing",
            ],
        },
        {
            "segment_name": "Enterprise & SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Cloud connectivity solutions",
                "Reliable business broadband",
            ],
            "pain_points": [
                "Limited B2B product portfolio",
                "Slow provisioning",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "SLA guarantees",
                "Price",
            ],
        },
    ],

    competitive_landscape_notes=[
        "3-player mobile market: Tigo (leader), Claro, Movistar",
        "Tigo dominates with ~50% mobile market share",
        "Prepaid-dominant market (~80% of connections)",
        "Growing HFC cable TV and broadband from Tigo",
        "Claro strong in postpaid and enterprise segments",
    ],

    pest_context={
        "political": [
            "Stable regulatory environment under SIT",
            "Government digital inclusion programs",
            "Free-market telecom policies",
        ],
        "economic": [
            "GDP growth ~3.5%, largest Central American economy",
            "Significant remittance economy (15% of GDP)",
            "Growing middle class driving smartphone adoption",
        ],
        "social": [
            "Young population (median age ~22)",
            "High mobile penetration, low fixed broadband",
            "Social media and messaging apps driving data usage",
        ],
        "technological": [
            "4G LTE deployment expanding",
            "Cable/HFC broadband growing in urban areas",
            "Mobile money services gaining traction",
        ],
    },
)
