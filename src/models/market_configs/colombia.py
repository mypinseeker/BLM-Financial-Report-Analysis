"""Colombia telecom market configuration."""

from src.models.market_config import MarketConfig

COLOMBIA_CONFIG = MarketConfig(
    market_id="colombia",
    market_name="Colombia",
    country="Colombia",
    currency="COP",
    currency_symbol="$",
    regulatory_body="CRC (Comision de Regulacion de Comunicaciones)",
    population_k=52000,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data plans for low-income users",
                "Rural and semi-urban coverage",
            ],
            "pain_points": [
                "Data runs out quickly",
                "Network congestion in Bogota/Medellin",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Social media bundles",
                "Recharge convenience",
            ],
        },
        {
            "segment_name": "Consumer Postpaid & Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "High-quality convergent bundles (mobile+fiber+TV)",
                "5G-ready plans",
            ],
            "pain_points": [
                "Slow fiber rollout outside major cities",
                "Complex pricing structures",
            ],
            "purchase_decision_factors": [
                "Bundle value",
                "Network speed",
                "Device offers",
                "Brand trust",
            ],
        },
        {
            "segment_name": "Enterprise Large",
            "segment_type": "enterprise",
            "unmet_needs": [
                "SD-WAN and multi-cloud connectivity",
                "IoT solutions for agriculture and logistics",
            ],
            "pain_points": [
                "Limited nationwide enterprise coverage",
                "Complex procurement processes",
            ],
            "purchase_decision_factors": [
                "National coverage",
                "SLA guarantees",
                "Managed services capability",
            ],
        },
        {
            "segment_name": "Enterprise SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Simple all-in-one business connectivity",
                "Affordable cloud solutions",
            ],
            "pain_points": [
                "High costs for business-grade internet",
                "Poor B2B customer service",
            ],
            "purchase_decision_factors": [
                "Price",
                "Simplicity",
                "Reliability",
            ],
        },
    ],

    competitive_landscape_notes=[
        "4-player market: Claro (leader), Movistar, Tigo, WOM (new entrant)",
        "Claro dominant with ~50% mobile share",
        "Tigo strong in cable TV and broadband via UNE acquisition",
        "WOM disrupting with aggressive pricing since 2020",
        "Active regulator (CRC) promoting competition",
        "Largest addressable market for Millicom in LATAM",
    ],

    pest_context={
        "political": [
            "CRC promoting infrastructure sharing",
            "Government MinTIC digital transformation agenda",
            "Spectrum auctions for 5G planned",
        ],
        "economic": [
            "GDP growth ~3.0%, second largest economy in LATAM after Brazil/Mexico",
            "Peso depreciation impacting equipment costs",
            "Growing middle class driving digital services demand",
        ],
        "social": [
            "52 million population, highly urbanized",
            "Strong social media and streaming adoption",
            "Digital divide between urban and rural areas",
        ],
        "technological": [
            "4G LTE covers ~90% of urban population",
            "5G trials underway, commercial launch expected soon",
            "Fiber broadband expanding rapidly in major cities",
            "Cable HFC infrastructure from Tigo-UNE merger",
        ],
    },
)
