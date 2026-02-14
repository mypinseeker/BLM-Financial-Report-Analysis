"""Belgium telecom market configuration."""

from src.models.market_config import MarketConfig

BELGIUM_CONFIG = MarketConfig(
    market_id="belgium",
    market_name="Belgium",
    country="Belgium",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="BIPT/IBPT (Belgian Institute for Postal Services and Telecommunications)",
    population_k=11759,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "Seamless multi-screen entertainment experience",
                "Ultra-fast symmetric broadband for remote work",
            ],
            "pain_points": [
                "High telecom prices compared to EU average",
                "Complex bundle structures across operators",
            ],
            "purchase_decision_factors": [
                "Bundle value (quad-play)",
                "Network speed and reliability",
                "TV content offering",
                "Brand reputation",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable convergent bundles",
                "Better mobile data allowances at reasonable prices",
            ],
            "pain_points": [
                "Belgium among most expensive EU markets for telecom",
                "Limited choice due to concentrated market",
            ],
            "purchase_decision_factors": [
                "Price-performance ratio",
                "Data volume",
                "Network coverage",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive / MVNO",
            "segment_type": "consumer",
            "unmet_needs": [
                "Low-cost mobile-only plans",
                "Prepaid flexibility without premium pricing",
            ],
            "pain_points": [
                "Limited MVNO competition compared to neighboring countries",
                "High entry-level pricing",
            ],
            "purchase_decision_factors": [
                "Lowest price",
                "No contract commitment",
                "Basic data included",
            ],
        },
        {
            "segment_name": "Enterprise & Government",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Private 5G networks for industrial sites",
                "Multi-cloud connectivity and cybersecurity",
                "IoT solutions for smart cities and logistics",
            ],
            "pain_points": [
                "Limited choice for large enterprise contracts",
                "Cross-border complexity (Belgium + Luxembourg)",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "Managed services capability",
                "National coverage (Flanders + Wallonia)",
                "International connectivity",
            ],
        },
    ],

    operator_bmc_enrichments={
        "proximus_be": {
            "key_resources": [
                "Largest fiber network in Belgium (2M+ homepass, accelerating)",
                "Comprehensive 5G mobile network (nationwide 3.5GHz rollout)",
                "Premium brand and largest enterprise customer base",
                "International presence via BICS (wholesale) and Telesur",
            ],
            "value_propositions": [
                "Belgium's most extensive fiber broadband network",
                "Premium quad-play convergent bundles (Proximus Flex)",
                "Leading enterprise ICT and cloud solutions (Proximus NXT)",
                "5G innovation and private network capabilities",
            ],
            "key_partners": [
                "Nokia (fiber and 5G deployment)",
                "Microsoft Azure (cloud partnership)",
                "BICS (international wholesale subsidiary)",
            ],
            "key_activities": [
                "Accelerated FTTH rollout (target 70% by 2028)",
                "5G standalone deployment and use case development",
                "Digital transformation under Bold2025 strategy",
                "Enterprise cloud and cybersecurity services growth",
            ],
        },
        "orange_be": {
            "key_resources": [
                "Orange Group technology and brand backing",
                "Growing mobile network with competitive 5G coverage",
                "Cable broadband infrastructure (via VOO/Brutele integration attempts)",
            ],
            "value_propositions": [
                "Competitive mobile pricing and value propositions",
                "Orange Group innovation and international roaming",
                "Growing convergent capability via network expansion",
            ],
            "key_partners": [
                "Orange Group (technology, procurement, brand)",
                "Ericsson (RAN vendor)",
            ],
            "key_activities": [
                "Mobile market share growth",
                "Developing convergent fixed-mobile offers",
                "5G network expansion",
                "Enterprise segment development",
            ],
        },
        "telenet_be": {
            "key_resources": [
                "Largest cable/HFC network in Flanders (3.4M homepass DOCSIS 3.1)",
                "VOO cable network in Wallonia (acquired 2023, 1.5M homepass)",
                "BASE mobile brand and network",
                "Strong entertainment content portfolio (Play, Play Sports)",
            ],
            "value_propositions": [
                "Fastest broadband via cable gigabit in Flanders",
                "Comprehensive entertainment bundles (TV + sports)",
                "Competitive mobile via BASE brand",
                "National cable coverage post-VOO acquisition",
            ],
            "key_partners": [
                "Liberty Global (majority owner, technology sharing)",
                "Fluvius (utility infrastructure access in Flanders)",
            ],
            "key_activities": [
                "VOO integration and Wallonia network upgrade",
                "DOCSIS 3.1 to 4.0 evolution",
                "National convergence strategy (Flanders + Wallonia)",
                "BASE mobile network improvement",
            ],
        },
    },

    operator_exposures={
        "proximus_be": [
            {
                "trigger_action": "Massive fiber investment program (multi-billion EUR over decade)",
                "side_effect": "Elevated capex constraining free cash flow and dividend capacity",
                "attack_vector": "Telenet already has nationwide cable broadband without comparable investment",
                "severity": "medium",
                "evidence": ["Fiber rollout accelerating but costly; target 70% coverage by 2028"],
            },
            {
                "trigger_action": "State ownership (53.5% Belgian government) limits strategic flexibility",
                "side_effect": "Political interference in strategic decisions and pricing",
                "attack_vector": "Private competitors can be more agile and commercially aggressive",
                "severity": "medium",
                "evidence": ["Belgian state majority shareholder; dividend expectations"],
            },
        ],
        "orange_be": [
            {
                "trigger_action": "Limited fixed broadband infrastructure",
                "side_effect": "Cannot offer competitive convergent bundles without own fixed network",
                "attack_vector": "Proximus and Telenet dominate convergent market with owned infrastructure",
                "severity": "high",
                "evidence": ["Failed VOO acquisition bid; relies on wholesale/resale for fixed broadband"],
            },
            {
                "trigger_action": "Smallest of three operators in converged market",
                "side_effect": "Scale disadvantage in content acquisition and infrastructure investment",
                "attack_vector": "Proximus and Telenet outspend on content and network",
                "severity": "medium",
                "evidence": ["Mobile-centric strategy in a convergence-driven market"],
            },
        ],
        "telenet_be": [
            {
                "trigger_action": "Liberty Global ownership review and potential strategic transactions",
                "side_effect": "Ownership uncertainty affecting long-term investment planning",
                "attack_vector": "Proximus capitalizes on uncertainty with aggressive convergent offers",
                "severity": "medium",
                "evidence": ["Liberty Global evaluating European asset portfolio"],
            },
            {
                "trigger_action": "VOO integration complexity (Wallonia cultural and operational differences)",
                "side_effect": "Integration costs and customer experience risks in Wallonia",
                "attack_vector": "Proximus strong in Wallonia where Telenet/VOO is integrating",
                "severity": "medium",
                "evidence": ["VOO acquired 2023; integration ongoing; different operating models"],
            },
        ],
    },

    operator_network_enrichments={
        "proximus_be": {
            "controlled_vs_resale": "Fully owned mobile + fixed network. Largest fiber network (2M+ homepass, targeting 4.2M). Legacy copper being retired. ~98% own-network.",
            "evolution_strategy": "Accelerated FTTH rollout partnering with Nokia; 5G standalone deployment; copper retirement; converged core network modernization; open fiber access where mandated.",
            "consumer_impact": "Best fiber broadband speeds; premium converged Proximus Flex bundles; widest 5G coverage; Proximus Pickx TV platform.",
            "b2b_impact": "Leading enterprise ICT provider in Belgium; Proximus NXT for cloud, cybersecurity, IoT; strong public sector presence; BICS for international wholesale.",
            "cost_impact": "Fiber rollout capex elevated but per-homepass costs declining; operational efficiency program (Bold2025); copper retirement saves long-term opex.",
            "org_culture": "Incumbent evolving under Bold2025 digital transformation; engineering excellence; strong social responsibility; complex stakeholder management (state ownership).",
        },
        "orange_be": {
            "controlled_vs_resale": "Fully owned mobile network. Limited fixed broadband infrastructure; relies on cable bitstream (regulated) and own fiber build in dense areas. ~70% mobile own-network, 30% fixed via wholesale.",
            "evolution_strategy": "5G rollout on 3.5 GHz; selective fiber deployment in dense areas; cable bitstream access for broadband; mobile-centric strategy with convergent ambitions.",
            "consumer_impact": "Competitive mobile pricing; growing 5G coverage; broadband via cable wholesale; innovative tariff structures with Orange Thank rewards.",
            "b2b_impact": "Growing enterprise segment leveraging Orange Group capabilities; IoT via Orange Business; managed connectivity services.",
            "cost_impact": "Lean cost structure as mobile-centric operator; Orange Group procurement advantages; wholesale access costs for fixed broadband.",
            "org_culture": "Agile challenger culture backed by Orange Group; commercially aggressive; digital innovation focus; relatively lean organization.",
        },
        "telenet_be": {
            "controlled_vs_resale": "Fully owned cable HFC network in Flanders (3.4M homepass) + VOO network in Wallonia (1.5M homepass). BASE mobile network (~85% own coverage). ~90% own-network overall.",
            "evolution_strategy": "DOCSIS 3.1→4.0 upgrade path; selective fiber overbuild in new build areas; VOO network modernization and integration; 5G via BASE mobile brand.",
            "consumer_impact": "Fastest broadband via cable gigabit in Flanders; comprehensive entertainment with Play Sports; growing national convergent proposition post-VOO.",
            "b2b_impact": "Business broadband via cable; growing enterprise segment; Telenet Business products for SME; limited large enterprise capability vs Proximus.",
            "cost_impact": "Cable upgrade capex lower than greenfield fiber; VOO integration costs elevated; Liberty Global shared services reduce overhead.",
            "org_culture": "Commercial and entertainment-focused culture; strong in content and customer experience; VOO integration bringing cultural evolution.",
        },
    },

    competitive_landscape_notes=[
        "3-player converged market: Proximus (incumbent), Telenet (cable/Flanders), Orange (mobile challenger)",
        "Among most expensive telecom markets in EU",
        "Convergence battle: Proximus fiber vs Telenet cable vs Orange mobile-centric",
        "Geographic split: Telenet dominant in Flanders, Proximus strongest nationally, Orange growing everywhere",
        "VOO acquisition by Telenet created national cable platform (Flanders+Wallonia)",
        "5G deployed by all three; Proximus leading in coverage",
        "BIPT promoting infrastructure competition and wholesale access",
    ],

    pest_context={
        "political": [
            "BIPT/IBPT regulation promoting competition and wholesale access",
            "Belgian state 53.5% ownership of Proximus shapes market dynamics",
            "EU Digital Decade targets driving broadband investment mandates",
            "5G spectrum auction completed 2022 (700/900/1800/2100/3600 MHz)",
        ],
        "economic": [
            "GDP per capita ~EUR 47,000; high purchasing power",
            "GDP growth ~1.0-1.5%; mature economy",
            "Automatic wage indexation increases operator cost base",
            "Brussels as EU institutional hub drives enterprise connectivity demand",
        ],
        "social": [
            "Population ~11.7M; bilingual market (Dutch/French)",
            "High smartphone penetration (~93%)",
            "Strong demand for convergent entertainment bundles",
            "Remote/hybrid work adoption driving broadband upgrade cycle",
        ],
        "technological": [
            "5G rollout by all three operators; coverage expanding 2024-2025",
            "Fiber FTTH rollout accelerating (Proximus targeting 70% by 2028)",
            "Cable DOCSIS 3.1 deployed nationally; 4.0 planned by Telenet",
            "IoT and smart city initiatives in Brussels, Antwerp, Ghent",
        ],
    },
)
