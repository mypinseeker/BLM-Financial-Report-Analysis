"""Ukraine telecom market configuration."""

from src.models.market_config import MarketConfig

UKRAINE_CONFIG = MarketConfig(
    market_id="ukraine",
    market_name="Ukraine",
    country="Ukraine",
    currency="UAH",
    currency_symbol="\u20b4",
    regulatory_body="NCEC / NKRZI (National Commission for State Regulation of Electronic Communications)",
    population_k=37000,

    customer_segments=[
        {
            "segment_name": "Consumer Urban Connected",
            "segment_type": "consumer",
            "unmet_needs": [
                "Reliable connectivity despite wartime infrastructure damage",
                "Affordable converged fixed-mobile bundles",
            ],
            "pain_points": [
                "Network outages from power grid attacks and conflict damage",
                "Limited fiber availability outside major cities",
            ],
            "purchase_decision_factors": [
                "Network reliability (critical in wartime)",
                "Price (cost-of-living pressures)",
                "Coverage breadth",
                "Customer service responsiveness",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive / Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Ultra-affordable prepaid data connectivity",
                "Resilient connectivity during power outages",
            ],
            "pain_points": [
                "Wartime economic pressure on household budgets",
                "Frequent network disruptions in eastern/southern regions",
            ],
            "purchase_decision_factors": [
                "Lowest price",
                "Prepaid flexibility",
                "Network availability during emergencies",
                "Coverage in conflict-affected areas",
            ],
        },
        {
            "segment_name": "Consumer Displaced / Refugee",
            "segment_type": "consumer",
            "unmet_needs": [
                "Easy number portability and activation in new locations",
                "Affordable roaming for those displaced abroad",
            ],
            "pain_points": [
                "Millions internally displaced; need connectivity in temporary locations",
                "Cross-border roaming costs for refugees in EU",
            ],
            "purchase_decision_factors": [
                "Activation ease",
                "Roaming affordability",
                "Coverage in western Ukraine (displacement hubs)",
            ],
        },
        {
            "segment_name": "Enterprise & Government",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Resilient communications infrastructure for businesses",
                "Cloud and cybersecurity services (heightened need)",
                "IoT for defense and critical infrastructure monitoring",
            ],
            "pain_points": [
                "Infrastructure damage affecting business connectivity",
                "Cybersecurity threats (state-sponsored attacks)",
            ],
            "purchase_decision_factors": [
                "Network resilience and redundancy",
                "Cybersecurity capability",
                "Service continuity guarantees",
                "Price competitiveness",
            ],
        },
    ],

    operator_bmc_enrichments={
        "lifecell_ua": {
            "key_resources": [
                "Mobile network covering major Ukrainian cities",
                "Datagroup-Volia fixed broadband network (#1 fixed ISP, ~4M HH)",
                "NJJ/Xavier Niel ownership — Western investment and technology access",
                "EBRD/IFC $435M financing for network modernization",
            ],
            "value_propositions": [
                "Ukraine's first converged telecom operator (mobile + fixed + TV)",
                "Western-backed operator with long-term investment commitment",
                "Competitive mobile plans targeting younger demographics",
                "Nationwide fixed broadband via Datagroup-Volia network",
            ],
            "key_partners": [
                "NJJ Holding / Xavier Niel (majority owner)",
                "Horizon Capital (co-investor)",
                "EBRD and IFC (development financing)",
                "Nokia (network equipment)",
            ],
            "key_activities": [
                "lifecell + Datagroup-Volia convergence and integration",
                "Network modernization and wartime resilience investment",
                "4G coverage expansion and densification",
                "Fixed broadband upgrade to fiber where possible",
            ],
        },
        "kyivstar_ua": {
            "key_resources": [
                "Ukraine's largest mobile network (~24M subscribers)",
                "Extensive 4G coverage (96%+ population)",
                "VEON Group technology platform and support",
                "Kyivstar TV and digital services ecosystem",
            ],
            "value_propositions": [
                "Ukraine's #1 mobile operator by subscribers and coverage",
                "Best network coverage including rural areas",
                "Kyivstar TV streaming and digital content",
                "Enterprise mobility solutions",
            ],
            "key_partners": [
                "VEON Group (parent company, Amsterdam-listed)",
                "Ericsson (RAN vendor)",
                "Google (digital services partnership)",
            ],
            "key_activities": [
                "Network resilience and wartime repair",
                "4G densification and coverage expansion",
                "Digital services (Kyivstar TV, Helsi health platform)",
                "Recovery from December 2023 cyberattack",
            ],
        },
        "vodafone_ua": {
            "key_resources": [
                "Comprehensive mobile network (~18M subscribers)",
                "Vodafone brand recognition and technology",
                "NEQSOL Holding backing (Azerbaijan-based)",
                "Strong digital services platform",
            ],
            "value_propositions": [
                "Trusted international brand in Ukraine",
                "Competitive mobile data plans",
                "SuperNet 4G advanced network",
                "Enterprise and IoT solutions",
            ],
            "key_partners": [
                "NEQSOL Holding (owner since 2019, Vodafone brand license)",
                "Huawei and Ericsson (RAN vendors)",
                "Vodafone Group (brand license only)",
            ],
            "key_activities": [
                "Network resilience and wartime operations",
                "4G network expansion",
                "Enterprise segment growth",
                "Digital transformation services",
            ],
        },
    },

    operator_exposures={
        "lifecell_ua": [
            {
                "trigger_action": "Active wartime environment with ongoing infrastructure damage",
                "side_effect": "Network outages, tower destruction, power grid attacks",
                "attack_vector": "Kyivstar and Vodafone have more redundant networks",
                "severity": "high",
                "evidence": ["Russia targeting Ukrainian energy and communications infrastructure"],
            },
            {
                "trigger_action": "Smallest mobile operator integrating newly acquired Datagroup-Volia",
                "side_effect": "Complex integration during wartime conditions",
                "attack_vector": "Kyivstar maintains scale advantage while lifecell is distracted",
                "severity": "medium",
                "evidence": ["NJJ completed lifecell+Datagroup-Volia acquisition Sep 2024; integration ongoing"],
            },
        ],
        "kyivstar_ua": [
            {
                "trigger_action": "Major cyberattack in December 2023 disrupted services for days",
                "side_effect": "Damaged customer trust and exposed vulnerability",
                "attack_vector": "lifecell and Vodafone gained temporary subscribers during outage",
                "severity": "medium",
                "evidence": ["Kyivstar suffered Russia-linked cyberattack Dec 2023; services down 3+ days"],
            },
            {
                "trigger_action": "VEON Group corporate complexity and sanctions risk",
                "side_effect": "Corporate governance concerns; VEON delisted from Amsterdam in 2024",
                "attack_vector": "NJJ-backed lifecell positions as stable Western-aligned operator",
                "severity": "medium",
                "evidence": ["VEON restructuring and re-domiciling; complex ownership history"],
            },
        ],
        "vodafone_ua": [
            {
                "trigger_action": "NEQSOL Holding (Azerbaijan) ownership raises geopolitical questions",
                "side_effect": "Less Western alignment than NJJ or even VEON post-restructuring",
                "attack_vector": "lifecell positions as EU-backed operator for enterprise customers",
                "severity": "low",
                "evidence": ["NEQSOL acquired Vodafone Ukraine 2019; Azerbaijani ownership"],
            },
            {
                "trigger_action": "Vodafone brand license — not a Vodafone Group subsidiary",
                "side_effect": "No Vodafone Group investment or technology sharing",
                "attack_vector": "Brand perception may not match reality of local ownership",
                "severity": "low",
                "evidence": ["Vodafone Group sold Ukraine operations to NEQSOL in 2019"],
            },
        ],
    },

    operator_network_enrichments={
        "lifecell_ua": {
            "controlled_vs_resale": "Owned mobile network covering major cities. Datagroup-Volia fixed broadband: #1 ISP with ~4M HH subscribers, own fiber/cable network. Combined ~85% own-network.",
            "evolution_strategy": "Converge lifecell mobile + Datagroup-Volia fixed into Ukraine's first integrated telco. EBRD/IFC $435M for network modernization. 4G densification. Fiber upgrade of Volia cable network.",
            "consumer_impact": "Competitive mobile plans. Growing convergent mobile+broadband+TV. Younger-skewing brand. Volia TV and broadband in major cities.",
            "b2b_impact": "Datagroup is Ukraine's #1 enterprise connectivity provider. Fiber backbone. Growing managed services. Government contracts.",
            "cost_impact": "NJJ acquisition cost $524M. EBRD/IFC financing available. Integration costs. Wartime network repair costs. Lean operations targeted.",
            "org_culture": "Transforming under Western ownership. Investment-focused despite wartime. Convergence-oriented. NJJ bringing Iliad Group operational know-how.",
        },
        "kyivstar_ua": {
            "controlled_vs_resale": "Fully owned mobile network. Ukraine's largest by coverage (96%+ pop). No owned fixed infrastructure. ~100% mobile own-network.",
            "evolution_strategy": "Network resilience and wartime repair. 4G densification. Digital services expansion (TV, health, fintech). Preparing for eventual 5G.",
            "consumer_impact": "Dominant mobile brand. Best coverage and reliability. Kyivstar TV streaming. Largest subscriber base gives strong network effects.",
            "b2b_impact": "Largest enterprise mobile provider. IoT solutions. Growing digital services. Government and defense contracts.",
            "cost_impact": "Scale advantages as market leader. VEON Group shared services. Wartime repair costs elevated. Strong cash generation despite war.",
            "org_culture": "Resilient wartime operations. VEON technology platform. Innovation in digital services. Post-cyberattack security focus.",
        },
        "vodafone_ua": {
            "controlled_vs_resale": "Fully owned mobile network. No owned fixed infrastructure. ~100% mobile own-network.",
            "evolution_strategy": "SuperNet 4G expansion. Network resilience improvements. Enterprise growth. Eventual 5G preparation.",
            "consumer_impact": "Strong mobile brand. Competitive data plans. Good urban coverage. SuperNet 4G quality.",
            "b2b_impact": "Growing enterprise segment. IoT solutions. Managed connectivity. Mid-market focus.",
            "cost_impact": "NEQSOL ownership provides financial stability. Moderate capex profile. Efficient operations.",
            "org_culture": "Vodafone brand values. NEQSOL management. Focused on mobile profitability.",
        },
    },

    competitive_landscape_notes=[
        "3-player mobile market: Kyivstar (#1 ~48% share), Vodafone Ukraine (#2 ~36%), lifecell (#3 ~16%)",
        "Wartime conditions fundamentally shape competitive dynamics — resilience is key differentiator",
        "lifecell + Datagroup-Volia merger creating Ukraine's first converged operator",
        "NJJ acquisition represents first major Western telecom investment in Ukraine since 2022 invasion",
        "No 5G deployment — spectrum not yet allocated, wartime priorities dominate",
        "Kyivstar December 2023 cyberattack was largest telecom disruption in European history",
        "Fixed broadband: Datagroup-Volia #1, Ukrtelecom #2 (state-owned), Kyivstar expanding",
        "NCEC regulation; spectrum allocation delayed by conflict",
    ],

    pest_context={
        "political": [
            "Active armed conflict with Russia since February 2022",
            "EU candidate status (granted June 2022) driving regulatory alignment",
            "Government prioritizing communications resilience as critical infrastructure",
            "Martial law in effect; some telecom regulation expedited",
            "5G spectrum allocation postponed due to conflict; military spectrum priorities",
        ],
        "economic": [
            "GDP ~USD 180B (2024); recovering from -29% contraction in 2022",
            "GDP growth ~3-4% (2024) — wartime recovery",
            "Inflation ~5-6% (2024, down from 20%+ in 2022)",
            "UAH/EUR exchange rate ~42-44; managed float",
            "International aid supporting economic stability (EU, US, IMF)",
        ],
        "social": [
            "Population ~37M within government-controlled territory (pre-war 44M)",
            "Millions internally displaced and 6M+ refugees abroad",
            "Smartphone penetration ~75-80%",
            "Digital services adoption accelerated by wartime needs (Diia app)",
            "Resilience and self-reliance mindset among population",
        ],
        "technological": [
            "4G coverage ~90%+ population by major operators",
            "No 5G deployment; spectrum allocation pending conflict resolution",
            "Fiber/broadband penetration ~50% of households",
            "Significant infrastructure damage from Russian attacks on energy/comms",
            "Starlink providing backup connectivity in conflict zones",
        ],
    },
)
