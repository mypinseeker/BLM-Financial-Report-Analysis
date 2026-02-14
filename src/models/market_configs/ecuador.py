"""Ecuador telecom market configuration."""

from src.models.market_config import MarketConfig

ECUADOR_CONFIG = MarketConfig(
    market_id="ecuador",
    market_name="Ecuador",
    country="Ecuador",
    currency="USD",
    currency_symbol="$",
    regulatory_body="ARCOTEL (Agencia de Regulacion y Control de las Telecomunicaciones)",
    population_k=18000,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable mobile data packages",
                "Better rural connectivity",
            ],
            "pain_points": [
                "Limited coverage outside major cities",
                "Expensive data relative to income",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Coverage area",
                "Social media bundles",
            ],
        },
        {
            "segment_name": "Consumer Postpaid Urban",
            "segment_type": "consumer",
            "unmet_needs": [
                "Higher speed 4G/LTE service",
                "Convergent fixed-mobile bundles",
            ],
            "pain_points": [
                "Network congestion in Quito and Guayaquil",
                "Limited device financing options",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "Data allowance",
                "Device availability",
                "Bundle value",
            ],
        },
        {
            "segment_name": "Enterprise & Government",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Cloud connectivity and managed services",
                "Reliable enterprise broadband",
            ],
            "pain_points": [
                "Limited B2B product sophistication",
                "Slow enterprise provisioning",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price",
                "SLA guarantees",
                "Local support",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_ecuador": {
            "key_resources": ["Former Telefonica Ecuador fixed+mobile network"],
            "value_propositions": ["Convergent bundles leveraging Millicom LATAM scale"],
            "key_partners": ["Millicom group shared services"],
            "key_activities": ["Network integration post-acquisition", "Brand transition to Tigo"],
        },
        "claro_ec": {
            "key_resources": ["Largest mobile subscriber base in Ecuador"],
            "value_propositions": ["Widest 4G coverage nationally", "Strong brand recognition"],
            "key_partners": ["America Movil group procurement"],
        },
        "cnt_ec": {
            "key_resources": ["State-owned fixed-line infrastructure", "Largest fiber network"],
            "value_propositions": ["Affordable broadband and telephony"],
            "key_activities": ["Government connectivity programs"],
        },
    },

    operator_exposures={
        "tigo_ecuador": [
            {
                "trigger_action": "Post-acquisition integration complexity from Telefonica Ecuador",
                "side_effect": "Customer churn during brand transition period",
                "attack_vector": "Claro and CNT target Tigo customers during transition",
                "severity": "high",
                "evidence": ["Recent acquisition still in integration phase"],
            },
            {
                "trigger_action": "Limited historical brand awareness as Tigo in Ecuador",
                "side_effect": "Customer trust deficit vs established Claro and CNT brands",
                "attack_vector": "Competitors emphasize local presence and stability",
                "severity": "medium",
                "evidence": ["New entrant brand in market"],
            },
        ],
        "claro_ec": [
            {
                "trigger_action": "Regulatory pressure on dominant operator market share",
                "side_effect": "Potential spectrum allocation restrictions",
                "attack_vector": "ARCOTEL pro-competition measures favor challengers",
                "severity": "medium",
                "evidence": ["ARCOTEL monitoring market concentration"],
            },
        ],
        "cnt_ec": [
            {
                "trigger_action": "State-owned operational inefficiency",
                "side_effect": "Slow innovation and service quality gaps",
                "attack_vector": "Private operators offer superior digital experience",
                "severity": "high",
                "evidence": ["Government budget constraints limit investment"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_ecuador": {
            "controlled_vs_resale": "Inherited Telefonica Ecuador fixed+mobile network; owns 4G mobile and fixed broadband infrastructure. ~85% own-network.",
            "evolution_strategy": "4G LTE expansion and densification; fiber rollout in major cities; integration with Millicom regional network standards.",
            "consumer_impact": "Convergent fixed-mobile capability inherited from Telefonica; transitioning brand and upgrading customer experience.",
            "b2b_impact": "Enterprise capabilities from Telefonica legacy; cloud and connectivity services; growing IoT portfolio.",
            "cost_impact": "Integration capex for network upgrades; Millicom group procurement advantages reduce equipment costs.",
            "org_culture": "Transitioning from Telefonica culture to Millicom/Tigo operational model; integration-focused management team.",
        },
        "claro_ec": {
            "controlled_vs_resale": "Fully owned mobile network; largest 4G coverage. ~95% self-built infrastructure.",
            "evolution_strategy": "4G LTE densification; expanding fixed broadband via fiber; 5G trials planned.",
            "consumer_impact": "Widest mobile coverage nationally; strong in both urban and semi-rural areas; leading device portfolio.",
            "b2b_impact": "Growing enterprise segment via America Movil group capabilities; cloud and data center services.",
            "cost_impact": "Scale advantages from America Movil group procurement; efficient per-subscriber costs.",
            "org_culture": "Competitive, results-driven culture; America Movil operational discipline; strong commercial execution.",
        },
        "cnt_ec": {
            "controlled_vs_resale": "State-owned nationwide fixed and mobile network; largest fiber infrastructure. ~100% own-network but aging copper plant.",
            "evolution_strategy": "Fiber expansion to secondary cities; 4G LTE coverage improvement; government digitalization backbone.",
            "consumer_impact": "Most affordable broadband options; widest fixed-line coverage; mobile quality below private operators.",
            "b2b_impact": "Government and public sector connectivity provider; limited commercial enterprise capabilities.",
            "cost_impact": "Government-funded infrastructure but constrained by public budget cycles; lower efficiency than private operators.",
            "org_culture": "Government bureaucratic culture; stable but slow-moving; public service mission oriented.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Claro (leader), Tigo (new via acquisition), CNT (state-owned)",
        "Dollarized economy (USD) simplifies cross-border comparison",
        "Prepaid-dominant mobile market (~70%)",
        "CNT dominates fixed broadband with state-owned infrastructure",
        "Tigo entry via Telefonica acquisition reshapes competitive dynamics",
    ],

    pest_context={
        "political": [
            "ARCOTEL regulatory oversight with pro-competition mandate",
            "Government digital transformation agenda",
            "Political instability concerns affecting investment climate",
        ],
        "economic": [
            "Dollarized economy, GDP growth ~2.5%",
            "Oil-dependent economy with fiscal constraints",
            "Growing digital economy and e-commerce adoption",
        ],
        "social": [
            "Young population, median age ~28",
            "High smartphone adoption in urban areas",
            "Digital divide between urban and rural populations",
        ],
        "technological": [
            "4G LTE deployment expanding to secondary cities",
            "Fiber broadband growing in Quito and Guayaquil",
            "5G spectrum allocation planned",
            "Mobile money and fintech adoption accelerating",
        ],
    },
)
