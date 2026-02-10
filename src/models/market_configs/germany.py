"""Germany telecom market configuration.

Migrated from hardcoded data in:
  - look_at_market_customer.py: GERMAN_TELECOM_SEGMENTS (L80-210)
  - look_at_self.py: operator BMC enrichments (L890-903) and exposures (L921-958)
"""

from src.models.market_config import MarketConfig

GERMANY_CONFIG = MarketConfig(
    market_id="germany",
    market_name="Germany",
    country="Germany",
    currency="EUR",
    currency_symbol="€",
    regulatory_body="BNetzA",
    population_k=84000,  # ~84 million

    # =========================================================================
    # Customer Segments (migrated from GERMAN_TELECOM_SEGMENTS)
    # =========================================================================
    customer_segments=[
        {
            "segment_name": "Consumer High-End",
            "segment_type": "consumer",
            "unmet_needs": [
                "Premium 5G standalone experiences",
                "Ultra-low latency gaming and VR",
            ],
            "pain_points": [
                "Network congestion in urban areas",
                "Limited premium content bundles",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "5G coverage",
                "Brand prestige",
                "Premium device availability",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better value convergent bundles",
                "Transparent pricing without hidden fees",
            ],
            "pain_points": [
                "Complex tariff structures",
                "Long contract lock-in periods",
            ],
            "purchase_decision_factors": [
                "Price-performance ratio",
                "Network reliability",
                "Bundle offers",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable unlimited data plans",
                "No-contract flexibility",
            ],
            "pain_points": [
                "Data caps at low price points",
                "Poor customer service at budget brands",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "No-contract options",
            ],
        },
        {
            "segment_name": "Consumer Youth",
            "segment_type": "consumer",
            "unmet_needs": [
                "Social media and streaming-optimized plans",
                "eSIM and digital-first experience",
            ],
            "pain_points": [
                "Expensive data top-ups",
                "Outdated app experiences",
            ],
            "purchase_decision_factors": [
                "Data volume",
                "App experience",
                "Social media bundles",
                "Price",
            ],
        },
        {
            "segment_name": "Enterprise Large",
            "segment_type": "enterprise",
            "unmet_needs": [
                "End-to-end managed SD-WAN",
                "Private 5G network solutions",
                "Multi-cloud connectivity",
            ],
            "pain_points": [
                "Complex multi-vendor management",
                "Slow provisioning times",
                "Lack of integrated security",
            ],
            "purchase_decision_factors": [
                "SLA guarantees",
                "Global coverage",
                "Security certifications",
                "Total cost of ownership",
                "Dedicated account management",
            ],
        },
        {
            "segment_name": "Enterprise SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Simple all-in-one business connectivity",
                "Affordable cloud and collaboration tools",
            ],
            "pain_points": [
                "IT resource constraints",
                "Complex B2B pricing",
                "Poor onboarding experience",
            ],
            "purchase_decision_factors": [
                "Simplicity",
                "Price",
                "Bundled IT services",
                "Local support",
            ],
        },
        {
            "segment_name": "Wholesale MVNO",
            "segment_type": "wholesale",
            "unmet_needs": [
                "Flexible wholesale pricing models",
                "Access to 5G network capabilities",
            ],
            "pain_points": [
                "Limited network differentiation",
                "Dependency on host MNO roadmap",
            ],
            "purchase_decision_factors": [
                "Wholesale rate",
                "Network quality access",
                "API availability",
                "Contract flexibility",
            ],
        },
    ],

    # =========================================================================
    # Operator BMC Enrichments (migrated from look_at_self.py L890-903)
    # =========================================================================
    operator_bmc_enrichments={
        "vodafone_germany": {
            "key_resources": ["Cable network (largest in Germany)"],
            "value_propositions": ["GigaCable Max ultra-fast broadband"],
        },
        "deutsche_telekom": {
            "key_partners": ["T-Mobile US (synergies)"],
            "key_resources": ["Largest fiber network in Germany"],
            "value_propositions": ["MagentaEINS convergence platform"],
        },
        "telefonica_o2": {
            "value_propositions": ["Value-for-money positioning"],
            "key_partners": ["Drillisch/1&1 (national roaming)"],
        },
        "one_and_one": {
            "key_activities": ["Network buildout (new entrant)"],
            "value_propositions": ["Disruptive pricing in mobile"],
        },
    },

    # =========================================================================
    # Operator Exposure Points (migrated from look_at_self.py L921-958)
    # =========================================================================
    operator_exposures={
        "vodafone_germany": [
            {
                "trigger_action": "1&1 building own mobile network and migrating users off Vodafone wholesale",
                "side_effect": "Loss of wholesale revenue as 1&1 users migrate to own network",
                "attack_vector": "1&1 positions as independent operator with competitive pricing",
                "severity": "high",
                "evidence": ["1&1 new entrant in Germany market", "Building Open RAN network"],
            },
            {
                "trigger_action": "Heavy reliance on cable (DOCSIS) technology while market shifts to fiber",
                "side_effect": "Technology perception gap as competitors lead fiber deployment",
                "attack_vector": "DT markets fiber superiority; cable seen as legacy",
                "severity": "high",
                "evidence": ["Cable-dominant broadband base", "DT aggressively deploying FTTH"],
            },
            {
                "trigger_action": "Low fiber penetration compared to Deutsche Telekom",
                "side_effect": "Competitive disadvantage in future-proof broadband",
                "attack_vector": "Customers migrating to FTTH offerings from DT",
                "severity": "medium",
                "evidence": ["Fiber subscriber base significantly smaller than cable"],
            },
        ],
        "deutsche_telekom": [
            {
                "trigger_action": "Massive fiber CAPEX investment requirement",
                "side_effect": "Margin pressure from infrastructure buildout",
                "attack_vector": "Competitors leverage existing cable infrastructure at lower cost",
                "severity": "medium",
                "evidence": ["Multi-billion EUR fiber rollout program"],
            },
        ],
        "telefonica_o2": [
            {
                "trigger_action": "Network perception gap despite 5G rollout",
                "side_effect": "Difficulty attracting premium segment customers",
                "attack_vector": "DT and Vodafone marketed as premium network operators",
                "severity": "medium",
                "evidence": ["Historically lower network quality scores"],
            },
        ],
        "one_and_one": [
            {
                "trigger_action": "Network buildout execution risk",
                "side_effect": "Dependence on national roaming from competitors during transition",
                "attack_vector": "Established operators can degrade wholesale terms",
                "severity": "high",
                "evidence": ["Open RAN network still in early deployment"],
            },
        ],
    },

    # =========================================================================
    # Competitive Landscape
    # =========================================================================
    competitive_landscape_notes=[
        "4-player market with DT as dominant incumbent",
        "1&1 new entrant building Open RAN network, transitioning from MVNO",
        "Cable vs fiber infrastructure competition between Vodafone and DT",
        "O2 aggressive on pricing, targeting mainstream/value segments",
        "Strong regulatory environment via BNetzA with pro-competition stance",
    ],

    # =========================================================================
    # PEST Context
    # =========================================================================
    pest_context={
        "political": [
            "BNetzA pro-competition regulatory framework",
            "EU Digital Markets Act affecting large telcos",
            "German government fiber expansion subsidies",
        ],
        "economic": [
            "GDP growth around 0.8%, slow recovery",
            "Inflation moderating to ~2%",
            "Energy costs impacting network OPEX",
        ],
        "social": [
            "High demand for digital services and home office connectivity",
            "Growing 5G awareness and adoption",
            "Price sensitivity in consumer market",
        ],
        "technological": [
            "5G SA rollout accelerating",
            "Fiber-to-the-home deployment race",
            "Open RAN technology adoption (1&1)",
            "Cable DOCSIS 4.0 upgrade path",
        ],
    },
)
