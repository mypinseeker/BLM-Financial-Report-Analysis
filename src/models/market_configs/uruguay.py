"""Uruguay telecom market configuration."""

from src.models.market_config import MarketConfig

URUGUAY_CONFIG = MarketConfig(
    market_id="uruguay",
    market_name="Uruguay",
    country="Uruguay",
    currency="UYU",
    currency_symbol="$U",
    regulatory_body="URSEC (Unidad Reguladora de Servicios de Comunicaciones)",
    population_k=3500,

    customer_segments=[
        {
            "segment_name": "Consumer Postpaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Higher mobile data speeds and allowances",
                "Better convergent fixed-mobile bundles",
            ],
            "pain_points": [
                "High prices relative to regional peers",
                "Limited provider choice vs Antel dominance",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "Data allowance",
                "Price",
                "Bundle value",
            ],
        },
        {
            "segment_name": "Consumer Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "More affordable data packages",
                "Flexible top-up options",
            ],
            "pain_points": [
                "Data cap frustration",
                "Limited prepaid plan variety",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Coverage",
                "Top-up convenience",
            ],
        },
        {
            "segment_name": "Enterprise & SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Cloud-integrated connectivity",
                "Managed IT services for SMEs",
            ],
            "pain_points": [
                "Antel near-monopoly in fixed enterprise",
                "Limited competitive alternatives",
            ],
            "purchase_decision_factors": [
                "Reliability",
                "Price",
                "Support quality",
                "Service breadth",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_uruguay": {
            "key_resources": ["Newly acquired mobile network assets"],
            "value_propositions": ["Competitive pricing vs Antel", "Millicom LATAM ecosystem integration"],
            "key_partners": ["Millicom group shared services"],
            "key_activities": ["Market entry and brand establishment", "Network investment"],
        },
        "antel_uy": {
            "key_resources": ["Nationwide fixed+mobile infrastructure", "100% fiber-to-the-home coverage", "State-owned monopoly on fixed"],
            "value_propositions": ["Most complete convergent offering", "Best network quality"],
            "key_activities": ["National broadband rollout", "5G deployment"],
        },
        "claro_uy": {
            "key_resources": ["Mobile network with 4G LTE coverage"],
            "value_propositions": ["Competitive mobile pricing", "International roaming via America Movil"],
            "key_partners": ["America Movil group procurement and synergies"],
        },
    },

    operator_exposures={
        "tigo_uruguay": [
            {
                "trigger_action": "New market entry competing against Antel state monopoly",
                "side_effect": "Limited fixed-line access constrains convergent offerings",
                "attack_vector": "Antel bundles fixed+mobile at subsidized prices",
                "severity": "high",
                "evidence": ["Antel controls ~100% of fixed broadband"],
            },
            {
                "trigger_action": "Small market size limits revenue potential",
                "side_effect": "Difficulty achieving scale economies in 3.5M population market",
                "attack_vector": "Antel and Claro already established with scale advantages",
                "severity": "medium",
                "evidence": ["Uruguay population ~3.5M, one of smallest Millicom markets"],
            },
        ],
        "antel_uy": [
            {
                "trigger_action": "State-owned complacency risk with new competitors entering",
                "side_effect": "Potential customer churn to more agile private operators",
                "attack_vector": "Tigo and Claro offer aggressive mobile pricing and digital experience",
                "severity": "low",
                "evidence": ["State monopoly on fixed protects core revenue"],
            },
        ],
        "claro_uy": [
            {
                "trigger_action": "Third-player squeeze between dominant Antel and new Tigo",
                "side_effect": "Market share pressure from both incumbent and new entrant",
                "attack_vector": "Tigo enters with aggressive pricing and Millicom investment",
                "severity": "medium",
                "evidence": ["#2 mobile operator facing new competition"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_uruguay": {
            "controlled_vs_resale": "Newly acquired mobile network; no fixed-line infrastructure. ~100% mobile own-network, fixed broadband via wholesale/resale only.",
            "evolution_strategy": "4G LTE densification and coverage expansion; potential 5G deployment; seeking fixed-access wholesale agreements.",
            "consumer_impact": "Mobile-focused offering; competitive pricing; limited fixed broadband capability constrains convergence.",
            "b2b_impact": "Early-stage enterprise segment; mobile-first B2B solutions; limited by lack of fixed infrastructure.",
            "cost_impact": "Acquisition investment with ongoing network buildout capex; Millicom group procurement benefits; subscale in small market.",
            "org_culture": "Startup/challenger mentality within Millicom framework; aggressive commercial posture; lean operations.",
        },
        "antel_uy": {
            "controlled_vs_resale": "State-owned nationwide fixed+mobile infrastructure; 100% FTTH coverage nationwide; owns all fixed infrastructure. ~100% own-network.",
            "evolution_strategy": "Already achieved 100% fiber coverage; 5G deployment underway; upgrading mobile to 5G SA; data center expansion.",
            "consumer_impact": "Best network quality in country; fastest broadband speeds; most complete convergent offering; premium service perception.",
            "b2b_impact": "Dominant enterprise provider; full suite of managed services; data center and cloud; government backbone.",
            "cost_impact": "Scale advantages from monopoly position; government-funded fiber rollout completed; 5G investment phase.",
            "org_culture": "State enterprise culture; technology-forward for LATAM state telco; strong engineering tradition; public service mandate.",
        },
        "claro_uy": {
            "controlled_vs_resale": "Own mobile network (4G LTE); no fixed infrastructure — mobile-only operator. ~100% own mobile network.",
            "evolution_strategy": "4G LTE densification; preparing for 5G spectrum; focused on mobile market share growth.",
            "consumer_impact": "Good mobile coverage and quality; competitive pricing; no fixed broadband offering.",
            "b2b_impact": "Mobile-focused B2B solutions; IoT via America Movil capabilities; limited by lack of fixed infrastructure.",
            "cost_impact": "Efficient mobile operations; America Movil group procurement advantages; no fixed infrastructure cost burden.",
            "org_culture": "America Movil operational discipline; competitive commercial culture; efficiency-focused.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Antel (state-owned dominant), Claro (#2), Tigo (new entrant)",
        "Antel has monopoly on fixed broadband with 100% FTTH coverage",
        "Mobile market more competitive with 3 operators",
        "Highest broadband quality in LATAM due to Antel fiber investment",
        "Small market (3.5M pop) limits revenue upside for entrants",
    ],

    pest_context={
        "political": [
            "URSEC regulatory oversight",
            "Government-backed digital inclusion via Antel",
            "Stable democratic governance supports investment",
        ],
        "economic": [
            "GDP growth ~3%, one of highest-income LATAM countries",
            "GDP per capita ~$18,000 USD, strong purchasing power",
            "Moderate inflation ~7%",
        ],
        "social": [
            "Highly urbanized population (~95%)",
            "High digital literacy and smartphone penetration",
            "Small population limits market scale",
        ],
        "technological": [
            "100% FTTH coverage via Antel — LATAM leader",
            "5G deployment underway",
            "Strong fixed broadband quality metrics",
            "High mobile internet adoption",
        ],
    },
)
