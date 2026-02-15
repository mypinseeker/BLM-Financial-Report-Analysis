"""Switzerland telecom market configuration."""

from src.models.market_config import MarketConfig

SWITZERLAND_CONFIG = MarketConfig(
    market_id="switzerland",
    market_name="Switzerland",
    country="Switzerland",
    currency="CHF",
    currency_symbol="CHF",
    regulatory_body="COMCOM / BAKOM (Federal Communications Commission / Federal Office of Communications)",
    population_k=8850,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "Seamless quad-play convergence at competitive prices",
                "True 10 Gbps fiber speeds delivered consistently",
            ],
            "pain_points": [
                "Very high telecom prices compared to EU neighbors",
                "Swisscom near-monopoly in fixed broadband limits choice",
            ],
            "purchase_decision_factors": [
                "Network quality and reliability",
                "Bundle value (fixed + mobile + TV)",
                "Brand trust and Swiss quality perception",
                "Customer service quality",
            ],
        },
        {
            "segment_name": "Consumer Value-Seeking",
            "segment_type": "consumer",
            "unmet_needs": [
                "More affordable unlimited mobile plans",
                "Better price-to-quality ratio vs EU benchmarks",
            ],
            "pain_points": [
                "Swiss telecom prices among highest in Europe",
                "Limited competitive pressure on pricing",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data volume and speed",
                "Network coverage (especially in mountains)",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Digital-First / Young",
            "segment_type": "consumer",
            "unmet_needs": [
                "eSIM and fully digital onboarding",
                "Flexible SIM-only plans with no contract",
            ],
            "pain_points": [
                "Traditional operators still require in-store visits",
                "Limited MVNO competition vs EU markets",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Digital experience (app, eSIM)",
                "No contract lock-in",
                "5G access",
            ],
        },
        {
            "segment_name": "Enterprise & SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Private 5G networks for pharmaceutical and financial sectors",
                "Cloud and cybersecurity managed services",
                "Multi-site SD-WAN connectivity",
            ],
            "pain_points": [
                "Swisscom dominates enterprise; limited alternatives",
                "High cost of dedicated circuits in Switzerland",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "Swiss data sovereignty (data stays in Switzerland)",
                "Managed services capability",
                "Price competitiveness",
            ],
        },
    ],

    operator_bmc_enrichments={
        "salt_ch": {
            "key_resources": [
                "Owned 4G/5G mobile network with nationwide coverage",
                "Growing FTTH fiber network (own-build + wholesale)",
                "Strong value-challenger brand positioning",
                "NJJ/Xavier Niel ownership — Iliad Group DNA and procurement synergies",
            ],
            "value_propositions": [
                "Best price-to-quality ratio in Swiss telecom",
                "10 Gbps fiber broadband (among first in Europe)",
                "Transparent pricing with no hidden fees",
                "Growing convergent fixed-mobile offering",
            ],
            "key_partners": [
                "NJJ Holding / Xavier Niel (sole owner)",
                "Nokia and Ericsson (RAN vendors)",
                "Swiss Fibre Net (fiber wholesale access)",
                "Scaleway (cloud infrastructure, Iliad Group)",
            ],
            "key_activities": [
                "5G network expansion and densification",
                "FTTH fiber rollout (own-build + wholesale access)",
                "Convergent bundle growth (Salt Home + Salt Mobile)",
                "Enterprise segment development",
            ],
        },
        "swisscom_ch": {
            "key_resources": [
                "Switzerland's largest fixed + mobile network (near-universal coverage)",
                "Dominant fiber network (3.5M+ FTTH homepass)",
                "Premium brand with highest customer trust",
                "51% Swiss Confederation ownership — sovereign backing",
            ],
            "value_propositions": [
                "Switzerland's #1 operator across all segments",
                "Premium network quality — best-in-class reliability",
                "Comprehensive convergent bundles (inOne)",
                "Leading enterprise ICT and cloud provider",
            ],
            "key_partners": [
                "Swiss Confederation (51% shareholder)",
                "Ericsson (5G RAN vendor)",
                "Microsoft/AWS (cloud partnerships)",
                "Fastweb + Vodafone Italia (Italian subsidiary)",
            ],
            "key_activities": [
                "Fiber FTTH expansion across Switzerland",
                "5G standalone deployment",
                "Enterprise digital transformation services",
                "Fastweb+Vodafone Italia integration in Italy",
            ],
        },
        "sunrise_ch": {
            "key_resources": [
                "Combined mobile + UPC cable/fiber network (post-merger)",
                "Largest cable TV subscriber base in Switzerland",
                "Strong brand in German-speaking Switzerland",
                "Liberty Global technology and content partnerships",
            ],
            "value_propositions": [
                "Comprehensive convergent operator (mobile + cable + fiber)",
                "Best TV and entertainment offering (UPC TV, Horizon platform)",
                "Competitive mobile plans with strong network",
                "Business solutions leveraging combined infrastructure",
            ],
            "key_partners": [
                "Liberty Global (parent company)",
                "Huawei and Nokia (RAN vendors)",
                "Netflix, Disney+ (content partnerships)",
            ],
            "key_activities": [
                "Post-merger integration and synergy extraction (Sunrise+UPC)",
                "Cable-to-fiber (DOCSIS 4.0 / FTTH) migration",
                "5G network expansion",
                "Convergent bundle growth",
            ],
        },
    },

    operator_exposures={
        "salt_ch": [
            {
                "trigger_action": "Limited owned fixed broadband infrastructure vs Swisscom",
                "side_effect": "Cannot compete on equal terms in fiber broadband",
                "attack_vector": "Swisscom and Sunrise leverage convergent advantage",
                "severity": "high",
                "evidence": ["Salt fiber footprint still much smaller than Swisscom's 3.5M+ FTTH homepass"],
            },
            {
                "trigger_action": "Smallest mobile operator in a 3-player market",
                "side_effect": "Scale disadvantage in procurement and content deals",
                "attack_vector": "Swisscom and Sunrise can outspend on network and marketing",
                "severity": "medium",
                "evidence": ["Salt ~16% mobile market share vs Swisscom ~55% and Sunrise ~25%"],
            },
        ],
        "swisscom_ch": [
            {
                "trigger_action": "Fastweb+Vodafone Italia integration consuming management attention",
                "side_effect": "Italian operations may distract from Swiss market defense",
                "attack_vector": "Salt and Sunrise gain ground while Swisscom focuses on Italy",
                "severity": "medium",
                "evidence": ["EUR 8B acquisition of Vodafone Italia closed Jan 2025; complex integration"],
            },
            {
                "trigger_action": "Premium pricing under pressure from Salt's aggressive offers",
                "side_effect": "ARPU erosion in consumer segment",
                "attack_vector": "Salt's Iliad DNA drives pricing pressure",
                "severity": "low",
                "evidence": ["Swiss mobile ARPU declining gradually; Salt offers significantly cheaper plans"],
            },
        ],
        "sunrise_ch": [
            {
                "trigger_action": "Post-merger Sunrise+UPC integration still ongoing",
                "side_effect": "Customer experience issues during system migration",
                "attack_vector": "Swisscom and Salt target churning customers",
                "severity": "medium",
                "evidence": ["Sunrise-UPC merger completed 2022 but full platform integration takes years"],
            },
            {
                "trigger_action": "Liberty Global may explore sale of Sunrise",
                "side_effect": "Ownership uncertainty could limit long-term investment",
                "attack_vector": "Swisscom positions as stable Swiss alternative",
                "severity": "low",
                "evidence": ["Liberty Global has history of selling assets; Sunrise IPO 2024"],
            },
        ],
    },

    operator_network_enrichments={
        "salt_ch": {
            "controlled_vs_resale": "Fully owned mobile network with 4G/5G nationwide coverage. Growing FTTH fiber via own-build + Swiss Fibre Net wholesale. ~100% mobile own-network, ~40% fixed via own fiber, 60% wholesale.",
            "evolution_strategy": "5G densification on 3.5 GHz. Aggressive FTTH build targeting major cities. 10 Gbps fiber services. Mobile-first evolving toward full convergence. Iliad Group technology sharing.",
            "consumer_impact": "Best value-for-money positioning. 10 Gbps fiber headline offer. Salt Home convergent bundles. Competitive unlimited mobile plans.",
            "b2b_impact": "Growing Salt Business segment. Enterprise mobile fleet management. Scaleway cloud partnership for B2B. Limited vs Swisscom in large enterprise.",
            "cost_impact": "Lean cost structure from Iliad/NJJ DNA. ~3,000 employees vs Swisscom's ~19,000. Best-in-class 60% EBITDA margin. NJJ procurement synergies.",
            "org_culture": "Challenger culture reinforced by NJJ/Niel ownership. Agile, commercially aggressive. Engineering-focused. Digital-first operations.",
        },
        "swisscom_ch": {
            "controlled_vs_resale": "Fully owned mobile + fixed network. Switzerland's largest fiber network (3.5M+ FTTH homepass). Near-universal copper/fiber coverage. ~98% own-network.",
            "evolution_strategy": "Fiber FTTH expansion targeting 4M+ homepass. 5G standalone deployment. Legacy copper retirement. Enterprise cloud growth. Italian expansion via Fastweb+Vodafone.",
            "consumer_impact": "Premium convergent operator. inOne bundles (mobile+broadband+TV). Best network quality perception. Highest ARPU in market.",
            "b2b_impact": "Switzerland's leading enterprise ICT provider. Cloud, cybersecurity, IoT. Government and financial sector contracts. Data center services.",
            "cost_impact": "Highest cost base (19K+ employees). Fiber capex elevated. Italian acquisition capex. Dividend commitment to Swiss Confederation constrains flexibility.",
            "org_culture": "Incumbent with strong Swiss quality values. Conservative, reliability-focused. Government ownership brings stability but limits agility.",
        },
        "sunrise_ch": {
            "controlled_vs_resale": "Fully owned mobile network + UPC cable/HFC network. Expanding fiber via DOCSIS upgrade + selective FTTH. ~90% own-network overall.",
            "evolution_strategy": "Cable-to-fiber migration (DOCSIS 4.0 + FTTH). 5G expansion. Post-merger network consolidation. Convergent growth leveraging combined base.",
            "consumer_impact": "Best TV/entertainment offering. Competitive convergent bundles. Strong in German-speaking Switzerland. UPC brand for cable customers.",
            "b2b_impact": "Sunrise Business for enterprise. Combined mobile+fixed for corporate. Growing but smaller than Swisscom enterprise.",
            "cost_impact": "Post-merger synergies being extracted. Cable network maintenance costs. Liberty Global shared services. Moderate cost structure.",
            "org_culture": "Post-merger integration phase. Liberty Global commercial culture. Innovation in TV/content. Ambitious convergent strategy.",
        },
    },

    competitive_landscape_notes=[
        "3-player market: Swisscom (dominant incumbent ~55% mobile), Sunrise (post-UPC merger ~25%), Salt (challenger ~16%)",
        "Among most expensive telecom markets in Europe — high ARPU but limited price competition",
        "Swisscom's 51% state ownership provides stability but regulatory scrutiny",
        "Salt applying Iliad Group disruptor playbook — aggressive pricing, lean operations",
        "Sunrise+UPC merger created a strong convergent #2 challenging Swisscom",
        "5G deployed by all three operators; Switzerland was early European adopter",
        "Fiber FTTH rollout accelerating; Swisscom leading, Salt growing via own-build",
        "Very limited MVNO presence; market essentially a 3-player oligopoly",
    ],

    pest_context={
        "political": [
            "COMCOM/BAKOM regulation; lighter touch than EU regulators",
            "Swisscom 51% state-owned — government telecom policy influence",
            "Switzerland not EU member; separate regulatory framework",
            "Strong data protection laws (nDSG revised 2023)",
            "5G spectrum allocated; no major pending auctions",
        ],
        "economic": [
            "GDP per capita ~CHF 92,000 (~EUR 95,000) — among world's highest",
            "GDP growth ~1.5% (2024); stable, mature economy",
            "Inflation ~1.5% (well-controlled)",
            "CHF/EUR exchange rate ~0.95; strong franc",
            "Very high consumer purchasing power supports premium pricing",
        ],
        "social": [
            "Population ~8.85M; growing moderately via immigration",
            "Smartphone penetration ~95%+",
            "Multilingual market (German 63%, French 23%, Italian 8%)",
            "High broadband penetration; fiber demand growing",
            "Remote/hybrid work well-established; drives connectivity demand",
        ],
        "technological": [
            "5G rollout by all three operators; among earliest in Europe",
            "Fiber FTTH coverage ~60%+ of premises (expanding rapidly)",
            "Swisscom targeting near-universal fiber by 2030",
            "Strong IoT and smart city adoption (Zurich, Geneva, Basel)",
            "Cloud and AI adoption high among Swiss enterprises",
        ],
    },
)
