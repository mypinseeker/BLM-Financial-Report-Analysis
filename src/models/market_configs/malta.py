"""Malta telecom market configuration."""

from src.models.market_config import MarketConfig

MALTA_CONFIG = MarketConfig(
    market_id="malta",
    market_name="Malta",
    country="Malta",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="MCA (Malta Communications Authority)",
    population_k=540,

    customer_segments=[
        {
            "segment_name": "Consumer Urban Connected",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster and more reliable broadband speeds",
                "Seamless converged fixed-mobile bundles",
            ],
            "pain_points": [
                "Small market with limited competition keeps prices moderate to high",
                "Cable/fiber transition creating service disruptions",
            ],
            "purchase_decision_factors": [
                "Network quality and speed",
                "Bundle value (fixed + mobile + TV)",
                "Brand trust and local reputation",
                "Coverage across Malta and Gozo",
            ],
        },
        {
            "segment_name": "Consumer Digital-First / Young",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable unlimited mobile data plans",
                "eSIM and digital-first onboarding",
            ],
            "pain_points": [
                "Limited mobile data allowances vs EU peers",
                "Slow eSIM adoption by local operators",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "5G access",
                "Digital experience",
                "No contract lock-in",
            ],
        },
        {
            "segment_name": "Tourist / Seasonal",
            "segment_type": "consumer",
            "unmet_needs": [
                "Easy tourist SIM and eSIM access",
                "Short-term data plans for visitors",
            ],
            "pain_points": [
                "Malta hosts 3M+ tourists annually for 540K population",
                "Roaming complexity for non-EU visitors",
            ],
            "purchase_decision_factors": [
                "Ease of purchase",
                "Coverage in tourist areas",
                "Short-term plan availability",
            ],
        },
        {
            "segment_name": "Enterprise & iGaming",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Low-latency connectivity for iGaming industry (Malta is EU iGaming hub)",
                "Cloud and cybersecurity managed services",
                "Reliable enterprise broadband",
            ],
            "pain_points": [
                "Limited choice for enterprise-grade connectivity",
                "Malta's small size limits data center scale",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "Price competitiveness",
                "Managed services capability",
                "Low latency for iGaming operations",
            ],
        },
    ],

    operator_bmc_enrichments={
        "epic_mt": {
            "key_resources": [
                "Owned mobile network with 4G/5G coverage",
                "Growing brand presence in Malta market",
                "Monaco Telecom/NJJ ownership — Xavier Niel telecom expertise",
                "Fiber broadband via wholesale access",
            ],
            "value_propositions": [
                "Competitive mobile plans challenging GO and Melita",
                "Growing 5G network coverage",
                "Digital-first mobile experience",
                "NJJ-backed investment commitment",
            ],
            "key_partners": [
                "Monaco Telecom / NJJ Holding (parent company)",
                "Network equipment vendors (Huawei)",
                "GO plc (wholesale fixed access)",
            ],
            "key_activities": [
                "5G network expansion",
                "Mobile subscriber acquisition and growth",
                "Fixed broadband growth via wholesale",
                "Brand building in Malta market",
            ],
        },
        "go_mt": {
            "key_resources": [
                "Malta's fixed-line infrastructure (copper + fiber)",
                "Comprehensive mobile network",
                "Listed on Malta Stock Exchange (GO plc)",
                "Subsidiary operations in Cyprus (Cablenet)",
            ],
            "value_propositions": [
                "Malta's leading convergent operator",
                "Comprehensive quad-play bundles (fixed + mobile + TV + broadband)",
                "Nationwide fixed and mobile coverage",
                "Enterprise ICT solutions",
            ],
            "key_partners": [
                "Listed company (Malta Stock Exchange)",
                "Cablenet Communications (Cyprus subsidiary)",
                "Network equipment vendors",
            ],
            "key_activities": [
                "Fiber FTTH network expansion",
                "5G mobile deployment",
                "Enterprise ICT and managed services",
                "Convergent bundle growth",
            ],
        },
        "melita_mt": {
            "key_resources": [
                "Cable/HFC network (largest cable footprint in Malta)",
                "Mobile network",
                "EQT ownership (Swedish PE firm)",
                "Strong TV and broadband subscriber base",
            ],
            "value_propositions": [
                "Best TV and entertainment offering in Malta",
                "Cable broadband speeds via DOCSIS upgrade",
                "Competitive convergent bundles",
                "Mobile + broadband + TV combo deals",
            ],
            "key_partners": [
                "EQT (PE owner since 2019)",
                "Liberty Global (technology partnerships)",
                "Content providers (TV channels)",
            ],
            "key_activities": [
                "Cable-to-fiber migration (DOCSIS 3.1 / FTTH)",
                "Mobile network improvement",
                "Convergent bundle competition",
                "Enterprise segment growth",
            ],
        },
    },

    operator_exposures={
        "epic_mt": [
            {
                "trigger_action": "Smallest operator in Malta's 3-player market",
                "side_effect": "Scale disadvantage in a tiny market (540K population)",
                "attack_vector": "GO and Melita have established fixed broadband bases",
                "severity": "high",
                "evidence": ["Epic Malta estimated ~15-20% mobile share; no owned fixed network"],
            },
            {
                "trigger_action": "No owned fixed broadband infrastructure",
                "side_effect": "Cannot offer competitive converged bundles independently",
                "attack_vector": "GO leverages fixed-mobile convergence; Melita has cable network",
                "severity": "high",
                "evidence": ["Epic relies on GO wholesale for any fixed broadband"],
            },
        ],
        "go_mt": [
            {
                "trigger_action": "Legacy copper network requires expensive FTTH migration",
                "side_effect": "Elevated capex constraining free cash flow",
                "attack_vector": "Melita's cable network provides broadband without copper replacement cost",
                "severity": "medium",
                "evidence": ["GO investing heavily in FTTH rollout across Malta"],
            },
            {
                "trigger_action": "Wholesale obligation means competitors benefit from GO's fiber",
                "side_effect": "Epic can offer broadband via GO wholesale at regulated prices",
                "attack_vector": "Epic gets broadband access without network build costs",
                "severity": "low",
                "evidence": ["MCA regulated wholesale access on GO's fixed network"],
            },
        ],
        "melita_mt": [
            {
                "trigger_action": "EQT PE ownership may lead to eventual sale",
                "side_effect": "Ownership uncertainty could limit long-term investment",
                "attack_vector": "GO and Epic position as committed long-term operators",
                "severity": "low",
                "evidence": ["EQT acquired Melita in 2019; typical PE hold period 5-7 years"],
            },
            {
                "trigger_action": "Cable network aging; requires DOCSIS upgrade or FTTH migration",
                "side_effect": "Technology transition costs and customer disruption risk",
                "attack_vector": "GO's fiber and Epic's 5G offer alternative high-speed access",
                "severity": "medium",
                "evidence": ["Melita transitioning from DOCSIS 3.0 to 3.1; FTTH selective"],
            },
        ],
    },

    operator_network_enrichments={
        "epic_mt": {
            "controlled_vs_resale": "Fully owned mobile network. No owned fixed infrastructure; wholesale access via GO. ~100% mobile own-network, 0% fixed own-network.",
            "evolution_strategy": "5G mobile expansion. Mobile-first strategy. Fixed broadband via wholesale. Brand growth in Malta.",
            "consumer_impact": "Growing mobile brand. Competitive pricing. Digital-first experience. 5G expanding.",
            "b2b_impact": "Limited enterprise presence. Mobile-focused B2B. Growing but smallest operator.",
            "cost_impact": "Lean mobile-only cost structure. NJJ procurement synergies. No fixed network capex.",
            "org_culture": "Monaco Telecom management. Private-sector agility. Challenger mindset.",
        },
        "go_mt": {
            "controlled_vs_resale": "Fully owned fixed + mobile network. Malta's national fixed-line incumbent. Fiber FTTH expanding. ~98% own-network.",
            "evolution_strategy": "FTTH fiber expansion. 5G deployment. Enterprise ICT growth. Cyprus expansion via Cablenet.",
            "consumer_impact": "Leading convergent operator. Quad-play bundles. Best fixed coverage. 46.8% broadband market share.",
            "b2b_impact": "Malta's leading enterprise ICT provider. Government contracts. Managed services.",
            "cost_impact": "Highest cost base as incumbent. Fiber capex elevated. Subsidiary costs (Cablenet). ~1,500 employees group-wide.",
            "org_culture": "Listed company culture. Professional management. Innovation in digital services. Regional ambitions (Cyprus).",
        },
        "melita_mt": {
            "controlled_vs_resale": "Fully owned cable/HFC network + mobile network. Cable covers most of Malta. ~90% own-network.",
            "evolution_strategy": "Cable-to-fiber migration (DOCSIS 3.1 + selective FTTH). Mobile improvement. Convergent growth.",
            "consumer_impact": "Best TV offering. Competitive convergent bundles. Cable broadband speeds. Strong brand loyalty.",
            "b2b_impact": "Growing enterprise segment. Cable-based enterprise connectivity. Limited vs GO in large enterprise.",
            "cost_impact": "EQT PE ownership driving efficiency. Cable network maintenance. Moderate cost structure.",
            "org_culture": "PE-owned commercial culture. Efficiency-driven. Investment in TV/content. Aggressive pricing.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: GO plc (#1, 34.8% mobile, 46.8% broadband), Melita (#2, cable+mobile), Epic (#3, mobile-centric)",
        "GO plc is Malta's fixed-line incumbent; listed on Malta Stock Exchange",
        "Melita owned by EQT (Swedish PE); cable/HFC network provides broadband alternative to GO fiber",
        "Epic owned by Monaco Telecom (NJJ/Xavier Niel); smallest operator, mobile-focused",
        "Very small market (540K pop) limits competitive intensity and investment scale",
        "5G deployed by all three operators; coverage expanding",
        "GO plc also operates Cablenet in Cyprus (cross-island strategy)",
        "iGaming industry drives enterprise connectivity demand (Malta is EU iGaming hub)",
    ],

    pest_context={
        "political": [
            "MCA (Malta Communications Authority) regulation; EU framework applies",
            "EU member state; full Digital Single Market rules",
            "Government supportive of digital transformation",
            "5G spectrum allocated; deployment underway",
            "iGaming regulation creates enterprise connectivity demand",
        ],
        "economic": [
            "GDP ~EUR 18B (2024); GDP per capita ~EUR 33,000",
            "GDP growth ~5% (2024); strong services-driven economy",
            "Inflation ~3% (2024)",
            "iGaming, tourism, and financial services drive economy",
            "Tourism: 3M+ visitors annually for 540K population",
        ],
        "social": [
            "Population ~540K; one of EU's smallest states",
            "Smartphone penetration ~90%+",
            "High digital literacy; bilingual (Maltese + English)",
            "Large expat community drives connectivity demand",
            "Dense urban areas; compact geography simplifies network deployment",
        ],
        "technological": [
            "5G deployed by all three operators",
            "Fiber/cable broadband covers most premises",
            "Dense geography enables efficient network deployment",
            "Malta as EU iGaming hub drives data center demand",
            "Smart city initiatives in development",
        ],
    },
)
