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

    operator_bmc_enrichments={
        "tigo_panama": {
            "key_resources": ["HFC cable network", "4G mobile coverage", "Tigo Money"],
            "value_propositions": ["Convergent mobile+cable+TV", "Enterprise connectivity for Canal Zone"],
            "key_partners": ["Millicom group", "Ericsson"],
            "key_activities": ["Cable broadband expansion", "Enterprise/logistics connectivity", "Data monetization"],
        },
        "claro_pa": {
            "key_resources": ["Largest mobile network", "Fiber broadband infrastructure", "Data center capabilities"],
            "value_propositions": ["Best coverage nationwide", "Enterprise solutions for banking/logistics"],
            "key_partners": ["America Movil group"],
        },
        "digicel_pa": {
            "key_resources": ["Mobile network"],
            "value_propositions": ["Budget mobile plans"],
        },
    },

    operator_exposures={
        "tigo_panama": [
            {
                "trigger_action": "Claro leads in mobile market share and 4G coverage",
                "side_effect": "Tigo positioned as #2 mobile, differentiation through fixed",
                "attack_vector": "Claro's fiber expansion erodes Tigo cable broadband advantage",
                "severity": "medium",
                "evidence": ["Claro 85% 4G vs Tigo 82%", "Claro fiber 400K HP vs Tigo 250K"],
            },
            {
                "trigger_action": "Small market size limits revenue growth potential",
                "side_effect": "4.4M population constrains subscriber growth ceiling",
                "attack_vector": "Market saturation approaching in mobile",
                "severity": "low",
                "evidence": ["Panama population ~4.4M", "High mobile penetration already"],
            },
        ],
        "claro_pa": [
            {
                "trigger_action": "Tigo's cable TV advantage in content bundling",
                "side_effect": "Claro lacks cable TV offering",
                "attack_vector": "Tigo bundles mobile+cable+TV at competitive prices",
                "severity": "medium",
                "evidence": ["Tigo cable TV market leader in Panama"],
            },
        ],
        "digicel_pa": [
            {
                "trigger_action": "Financial distress and market exit risk",
                "side_effect": "Continued subscriber decline",
                "attack_vector": "Tigo and Claro absorb departing Digicel customers",
                "severity": "high",
                "evidence": ["Digicel Group restructuring", "Declining subscribers"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_panama": {
            "controlled_vs_resale": "Fully owned mobile 4G + HFC cable network (450K homes). ~95% self-built.",
            "evolution_strategy": "4G LTE densification; fiber overlay in Panama City; cable DOCSIS 3.1; enterprise connectivity for Canal Zone.",
            "consumer_impact": "Strong convergent bundle; cable broadband up to 300 Mbps; good 4G coverage; high-ARPU market.",
            "b2b_impact": "Enterprise connectivity for Canal/logistics corridor; Tigo Business for SMEs; data center partnership.",
            "cost_impact": "Cable efficient for broadband; compact geography; Millicom procurement; high ARPU supports investment.",
            "org_culture": "High-performing small market; Millicom standards; enterprise-oriented; innovative in fintech.",
        },
        "claro_pa": {
            "controlled_vs_resale": "Own mobile 4G + fiber broadband. ~93% self-built.",
            "evolution_strategy": "Fiber broadband expansion; 4G densification; data center services.",
            "consumer_impact": "Best mobile coverage; growing fiber broadband; premium positioning.",
            "b2b_impact": "Strongest enterprise portfolio — data center, cloud, managed services; Canal Zone enterprise.",
            "cost_impact": "America Movil procurement; scale advantages; fiber investment ongoing.",
            "org_culture": "America Movil discipline; enterprise-focused; market leader position.",
        },
        "digicel_pa": {
            "controlled_vs_resale": "Own mobile network, ~42% 4G coverage. No fixed. Declining.",
            "evolution_strategy": "Maintenance mode; potential exit.",
            "consumer_impact": "Budget pricing; poor quality; declining.",
            "b2b_impact": "None.",
            "cost_impact": "Minimal investment; network degradation.",
            "org_culture": "Survival mode; group financial distress.",
        },
    },

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
