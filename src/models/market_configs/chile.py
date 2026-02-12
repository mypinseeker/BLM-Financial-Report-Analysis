"""Chile telecom market configuration."""

from src.models.market_config import MarketConfig

CHILE_CONFIG = MarketConfig(
    market_id="chile",
    market_name="Chile",
    country="Chile",
    currency="CLP",
    currency_symbol="$",
    regulatory_body="SUBTEL (Subsecretaria de Telecomunicaciones)",
    population_k=19500,

    customer_segments=[
        {
            "segment_name": "Consumer Postpaid Premium",
            "segment_type": "consumer",
            "unmet_needs": [
                "5G coverage and experiences",
                "Premium convergent bundles (fiber+mobile+streaming)",
            ],
            "pain_points": [
                "5G deployment slower than expected",
                "Complex multi-play pricing",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "5G availability",
                "Bundle value",
                "Brand perception",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better value mobile plans",
                "Reliable home broadband",
            ],
            "pain_points": [
                "Price competition driving confusion",
                "Service quality inconsistency",
            ],
            "purchase_decision_factors": [
                "Price-performance ratio",
                "Data volume",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive",
            "segment_type": "consumer",
            "unmet_needs": [
                "Ultra-low-cost data plans",
                "No-contract flexibility",
            ],
            "pain_points": [
                "WOM disruption raising expectations",
                "Data caps at budget tier",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "No-contract options",
            ],
        },
        {
            "segment_name": "Enterprise Large",
            "segment_type": "enterprise",
            "unmet_needs": [
                "SD-WAN and multi-cloud solutions",
                "Private 5G for mining and logistics",
            ],
            "pain_points": [
                "Limited 5G enterprise solutions",
                "High cost of dedicated circuits",
            ],
            "purchase_decision_factors": [
                "Network reliability",
                "SLA guarantees",
                "Innovation capability",
            ],
        },
        {
            "segment_name": "Enterprise SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Simple all-in-one business solutions",
                "Affordable cloud hosting",
            ],
            "pain_points": [
                "Complex B2B pricing",
                "Slow provisioning",
            ],
            "purchase_decision_factors": [
                "Price",
                "Simplicity",
                "Reliability",
            ],
        },
    ],

    operator_bmc_enrichments={
        "entel_cl": {
            "key_partners": [
                "Nokia (5G SA core)", "Ericsson (RAN)",
                "BHP/Codelco (enterprise private 5G)"
            ],
            "key_resources": [
                "4,200 owned towers (largest in Chile)",
                "First 5G SA network in Chile",
                "Premium brand positioning"
            ],
            "key_activities": [
                "5G SA deployment and enterprise private networks",
                "Copper-to-fiber migration program",
                "Digital services (cloud, cybersecurity)"
            ],
            "value_propositions": [
                "Best network quality (Opensignal #1)",
                "Convergent fiber+mobile bundles",
                "Enterprise private 5G for mining"
            ],
        },
        "movistar_cl": {
            "key_partners": [
                "Telefonica Group (global enterprise)", "Amazon (cloud partnership)"
            ],
            "key_resources": [
                "Largest FTTH network: 3.5M homes passed",
                "Telefonica global enterprise contracts"
            ],
            "key_activities": [
                "FTTH expansion to 4.5M homes",
                "Convergent (Fusión) bundle strategy"
            ],
            "value_propositions": [
                "Best fiber broadband coverage",
                "Movistar Fusión convergent bundles",
                "Global enterprise solutions via Telefonica"
            ],
        },
        "claro_cl": {
            "key_partners": [
                "América Móvil (group synergies)", "Claro TV+ (content)"
            ],
            "key_resources": [
                "América Móvil financial backing",
                "Largest retail distribution network in Chile"
            ],
            "key_activities": [
                "$300M 5G+fiber investment plan (2025-2026)",
                "Transition from mobile-only to convergent model"
            ],
            "value_propositions": [
                "Aggressive pricing powered by América Móvil scale",
                "Wide retail distribution and brand recognition"
            ],
        },
        "wom_cl": {
            "key_partners": [
                "New investor consortium (post-restructuring)"
            ],
            "key_resources": [
                "7.2M mobile subscribers",
                "Strong brand among youth/price-sensitive segments",
                "5G spectrum holdings"
            ],
            "key_activities": [
                "Debt restructuring execution",
                "5G deployment with reduced capex",
                "Disruptive pricing strategy"
            ],
            "value_propositions": [
                "Lowest-price mobile data plans in Chile",
                "Digital-first customer experience",
                "Youth-oriented brand positioning"
            ],
        },
        "tigo_chile": {
            "key_partners": [
                "Entel (MVNO network access)"
            ],
            "key_resources": [
                "Millicom group enterprise capabilities",
                "LATAM regional presence"
            ],
            "key_activities": [
                "MVNO model execution on Entel network",
                "Enterprise B2B segment focus"
            ],
            "value_propositions": [
                "Niche enterprise and digital services",
                "Millicom group cross-border solutions"
            ],
        },
    },

    operator_exposures={
        "entel_cl": [
            {
                "trigger_action": "5G SA investment competing with established players",
                "attack_vector": "Movistar's fiber footprint advantage in broadband",
                "side_effect": "Capex pressure during 5G build-out phase (17-19% capex/revenue)",
                "severity": "medium",
                "evidence": [
                    "$120M 5G investment in 2025",
                    "Movistar has 3.5M FTTH homes vs Entel 2.8M"
                ],
            },
            {
                "trigger_action": "WOM's post-restructuring competitive aggression",
                "attack_vector": "WOM emerges with $800M less debt, renewed pricing war capability",
                "side_effect": "ARPU pressure in price-sensitive segments",
                "severity": "high",
                "evidence": [
                    "WOM historically triggered 30% ARPU erosion since 2015 entry",
                    "Post-restructuring WOM has lower debt service costs"
                ],
            },
            {
                "trigger_action": "Mining sector cyclicality affecting enterprise revenue",
                "attack_vector": "Copper price decline could reduce mining capex including telecom",
                "side_effect": "Enterprise segment (28% of revenue) exposed to commodity cycles",
                "severity": "medium",
                "evidence": [
                    "Enterprise revenue grew 8.5% driven by mining contracts",
                    "Copper prices at cyclical highs"
                ],
            },
        ],
        "movistar_cl": [
            {
                "trigger_action": "Telefonica Group financial constraints",
                "attack_vector": "Parent company debt and divestiture pressure could limit Chile investment",
                "side_effect": "Potential underinvestment in 5G if Group prioritizes other markets",
                "severity": "medium",
                "evidence": [
                    "Telefonica global debt >€30B",
                    "Group has sold LATAM assets in past"
                ],
            },
            {
                "trigger_action": "Copper network sunset costs",
                "attack_vector": "Legacy copper network maintenance costs while migrating to fiber",
                "side_effect": "Dual-network operating costs during transition period",
                "severity": "medium",
                "evidence": [
                    "Still operating copper DSL for legacy customers",
                    "FTTH migration incomplete"
                ],
            },
        ],
        "claro_cl": [
            {
                "trigger_action": "Late entry to convergent market",
                "attack_vector": "Entel and Movistar already have established fiber+mobile bundles",
                "side_effect": "Difficult to win converged customers from established competitors",
                "severity": "high",
                "evidence": [
                    "Claro historically mobile-focused with limited fixed",
                    "$300M investment plan tries to close gap but competitors years ahead"
                ],
            },
        ],
        "wom_cl": [
            {
                "trigger_action": "Post-restructuring execution risk",
                "attack_vector": "New investors may prioritize short-term returns over long-term network investment",
                "side_effect": "Network quality deterioration if capex is cut",
                "severity": "high",
                "evidence": [
                    "Just emerged from Chapter 11",
                    "New investor consortium is financial, not strategic"
                ],
            },
            {
                "trigger_action": "No fixed broadband network",
                "attack_vector": "Cannot offer convergent bundles that reduce churn",
                "side_effect": "Higher mobile churn vs converged competitors",
                "severity": "medium",
                "evidence": [
                    "WOM is mobile-only operator",
                    "Convergent competitors show 40% lower churn"
                ],
            },
        ],
        "tigo_chile": [
            {
                "trigger_action": "Sub-3% market share in hyper-competitive market",
                "attack_vector": "Too small to compete on price or network investment",
                "side_effect": "Strategic review may lead to market exit",
                "severity": "high",
                "evidence": [
                    "Pivoted to MVNO model",
                    "Returned spectrum to SUBTEL"
                ],
            },
        ],
    },

    # =========================================================================
    # Operator Network Enrichments (for NetworkAnalysis + org_culture)
    # =========================================================================
    operator_network_enrichments={
        "entel_cl": {
            "controlled_vs_resale": "Fully integrated operator: 4,200 owned towers, own fiber+copper fixed network, 5G SA mobile. ~95% self-built infrastructure.",
            "evolution_strategy": "5G SA leader (Nokia core); copper-to-fiber migration; 2.8M FTTH homes passed target 3.5M by 2027; private 5G for mining sector.",
            "consumer_impact": "Best network quality (Opensignal #1); strong 5G coverage in major cities; fiber+mobile convergent bundles; premium positioning.",
            "b2b_impact": "Enterprise leader via private 5G for mining (BHP, Codelco); SD-WAN and cloud services; IoT platform for industrial verticals; 28% revenue from enterprise.",
            "cost_impact": "Capex intensity 17-19% driven by 5G SA + fiber; tower ownership provides long-term cost advantage; scale benefits as market leader.",
            "org_culture": "Innovation-led culture; strong engineering focus; premium brand DNA; long-tenured leadership team; Chilean market champion identity.",
        },
        "movistar_cl": {
            "controlled_vs_resale": "Own fiber (largest FTTH: 3.5M homes passed) + copper legacy; mobile own-network; ~90% self-built, some rural wholesale.",
            "evolution_strategy": "FTTH expansion to 4.5M homes by 2027; copper sunset roadmap; 5G deployment (NSA first, SA planned); convergent Fusión strategy.",
            "consumer_impact": "Best broadband coverage (fiber leader); Movistar Fusión convergent bundles; 5G rollout underway but behind Entel; copper legacy in some areas.",
            "b2b_impact": "Telefonica Global Enterprise contracts; cloud via Telefonica Tech; growing B2B but behind Entel in mining verticals; SD-WAN available.",
            "cost_impact": "Dual copper+fiber network transition costs; Telefonica Group efficiency programs driving opex reduction; capex focused on FTTH expansion.",
            "org_culture": "Telefonica Group culture — global processes with local execution; convergent strategy focus; efficiency-driven transformation; union workforce.",
        },
        "claro_cl": {
            "controlled_vs_resale": "Own mobile network; limited fixed infrastructure — building out fiber; ~70% own-network, ~30% wholesale/resale in fixed.",
            "evolution_strategy": "$300M 5G+fiber investment plan (2025-2026); transitioning from mobile-dominant to convergent model; 5G deployment accelerating.",
            "consumer_impact": "Strong mobile coverage; aggressive pricing powered by América Móvil scale; fiber broadband expanding but smaller footprint than Entel/Movistar.",
            "b2b_impact": "Growing enterprise via América Móvil group capabilities; Claro Empresas; limited vs Entel in mining/industrial verticals.",
            "cost_impact": "Heavy investment period ($300M plan); América Móvil financial backing provides investment capacity; mobile network is cost-efficient at scale.",
            "org_culture": "América Móvil group culture — cost-discipline and operational efficiency; aggressive commercial posture; rapid execution capability; Mexican group DNA.",
        },
        "wom_cl": {
            "controlled_vs_resale": "Mobile-only operator; own mobile network + 5G spectrum; no fixed infrastructure. 100% own mobile, 0% fixed.",
            "evolution_strategy": "5G deployment with reduced capex post-restructuring; no fixed broadband plans; FWA could provide limited home broadband alternative.",
            "consumer_impact": "Disruptive pricing champion; strong brand among youth; mobile-only means no convergent bundles; 5G expanding but coverage behind Entel.",
            "b2b_impact": "Minimal B2B presence; no enterprise portfolio; mobile-only limits B2B use cases; potential in SME mobile fleet management.",
            "cost_impact": "Post-restructuring with $800M less debt; lower debt service enables more network investment; but no fixed amortization base.",
            "org_culture": "Disruptor DNA; aggressive commercial culture; youth-oriented brand; post-restructuring new investor influence; lean operations with digital-first approach.",
        },
        "tigo_chile": {
            "controlled_vs_resale": "MVNO model on Entel network; returned own spectrum to SUBTEL; 100% resale/virtual operation.",
            "evolution_strategy": "Pivoted from MNO to MVNO; focused on enterprise niche and B2B services; leveraging Millicom group capabilities.",
            "consumer_impact": "Minimal consumer presence; sub-3% market share; niche positioning; dependent on Entel network quality.",
            "b2b_impact": "Enterprise focus via Millicom group capabilities; LATAM cross-border B2B solutions; limited scale for large enterprise deals.",
            "cost_impact": "MVNO model is capex-light but margin-constrained by wholesale rates; Millicom group provides shared service efficiencies.",
            "org_culture": "Millicom group culture — LATAM-focused, entrepreneurial; strategic review mindset in Chile; niche operator identity.",
        },
    },

    competitive_landscape_notes=[
        "5-player market: Entel, Movistar, Claro, WOM, Tigo (smallest)",
        "WOM disrupted market since 2015 with aggressive pricing",
        "Entel leads in premium mobile, Movistar in convergent",
        "Chile most competitive LATAM telecom market",
        "Tigo has smallest market share, partnership/MVNO model",
        "5G launched by Entel, WOM, Movistar",
    ],

    pest_context={
        "political": [
            "SUBTEL active in spectrum allocation and competition",
            "New constitution process affecting regulatory framework",
            "Government pushing 5G deployment",
        ],
        "economic": [
            "GDP growth ~2.5%, highest GDP per capita in LATAM",
            "Peso volatility affecting equipment costs",
            "Mature consumer economy",
        ],
        "social": [
            "High smartphone penetration (~85%)",
            "Strong streaming and digital services adoption",
            "Demanding consumers with high service expectations",
        ],
        "technological": [
            "5G commercial launch in major cities",
            "Fiber broadband expanding rapidly",
            "Most advanced telecom market in LATAM",
            "High 4G penetration (~90%)",
        ],
    },
)
