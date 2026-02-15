"""Ireland telecom market configuration."""

from src.models.market_config import MarketConfig

IRELAND_CONFIG = MarketConfig(
    market_id="ireland",
    market_name="Ireland",
    country="Ireland",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="ComReg (Commission for Communications Regulation)",
    population_k=5150,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "Reliable high-speed fiber across all of Ireland (rural gap)",
                "Seamless fixed-mobile convergent bundles",
            ],
            "pain_points": [
                "Rural broadband still patchy despite National Broadband Plan",
                "Limited convergent offerings vs UK/continental markets",
            ],
            "purchase_decision_factors": [
                "Network reliability and speed",
                "Bundle value (fixed + mobile + TV)",
                "Brand trust",
                "Local availability of fiber",
            ],
        },
        {
            "segment_name": "Consumer Value-Seeking",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable unlimited mobile data plans",
                "Transparent pricing without bill shock",
            ],
            "pain_points": [
                "Three's dominance limits pricing competition",
                "Confusing tariff structures across operators",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "Network coverage (especially rural Ireland)",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Digital-First / Young",
            "segment_type": "consumer",
            "unmet_needs": [
                "eSIM and digital-first onboarding",
                "Flexible SIM-only plans",
            ],
            "pain_points": [
                "Limited 5G coverage outside Dublin/Cork",
                "Slow eSIM adoption by Irish operators",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "5G access",
                "Digital experience",
                "No contract lock-in",
            ],
        },
        {
            "segment_name": "Enterprise & Public Sector",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Reliable connectivity for multinational HQs (Ireland is EU tech hub)",
                "Private 5G for pharmaceutical manufacturing",
                "Cloud and cybersecurity managed services",
            ],
            "pain_points": [
                "Enterprise fiber limited outside Dublin business districts",
                "Lack of scale in managed services vs UK/EU providers",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "National coverage",
                "Managed services capability",
                "Data sovereignty (EU/Irish data residency)",
            ],
        },
    ],

    operator_bmc_enrichments={
        "eir_ie": {
            "key_resources": [
                "Ireland's fixed-line network owner (2.2M premises FTTH/FTTC)",
                "Comprehensive mobile + fixed infrastructure",
                "Wholesale revenue from all competitors using eir network",
                "NJJ/Xavier Niel ownership (>70%) — Iliad Group operational DNA",
            ],
            "value_propositions": [
                "Ireland's only truly converged fixed+mobile operator with own infrastructure",
                "Fastest fiber speeds via own FTTH network",
                "Premium brand backed by nationwide infrastructure",
                "Growing enterprise ICT solutions",
            ],
            "key_partners": [
                "NJJ Holding / Xavier Niel (>70% owner)",
                "Nokia (RAN and fiber equipment)",
                "National Broadband Ireland (NBP contract partner)",
                "Apple, Samsung (device partnerships)",
            ],
            "key_activities": [
                "FTTH network expansion (targeting 95%+ coverage)",
                "5G mobile network rollout",
                "Wholesale services to competitors (open eir)",
                "Enterprise digital transformation services",
            ],
        },
        "three_ie": {
            "key_resources": [
                "Ireland's largest mobile subscriber base (~48% share)",
                "Comprehensive 4G/5G mobile network",
                "CK Hutchison financial backing",
                "Strong brand in prepaid and youth segments",
            ],
            "value_propositions": [
                "Ireland's mobile market leader",
                "Competitive unlimited data plans",
                "All You Can Eat (AYCE) data pioneered in Ireland",
                "Growing 5G network",
            ],
            "key_partners": [
                "CK Hutchison (parent company)",
                "Ericsson (RAN vendor)",
                "eir (wholesale fiber access for broadband)",
            ],
            "key_activities": [
                "Mobile network leadership and 5G expansion",
                "Fixed broadband growth via wholesale fiber",
                "Brand positioning for unlimited data",
                "Cost optimization",
            ],
        },
        "vodafone_ie": {
            "key_resources": [
                "Comprehensive mobile network (5G expanding)",
                "Vodafone Group technology and brand",
                "Strong enterprise customer base",
                "SIRO JV (50% with ESB) — fiber infrastructure",
            ],
            "value_propositions": [
                "Premium mobile network quality",
                "Enterprise solutions leveraging Vodafone Group",
                "Converging fixed-mobile via SIRO fiber",
                "Global brand trust",
            ],
            "key_partners": [
                "Vodafone Group (parent company)",
                "ESB (SIRO fiber JV partner)",
                "eir (wholesale access)",
                "Microsoft (enterprise cloud)",
            ],
            "key_activities": [
                "5G network expansion",
                "SIRO fiber rollout for broadband",
                "Enterprise and IoT services growth",
                "Convergent bundle development",
            ],
        },
    },

    operator_exposures={
        "eir_ie": [
            {
                "trigger_action": "Heavy capex burden from FTTH network rollout",
                "side_effect": "Elevated investment constraining free cash flow",
                "attack_vector": "Three and Vodafone compete with lower capital intensity using eir wholesale",
                "severity": "medium",
                "evidence": ["eir investing heavily in FTTH targeting 95%+ of Ireland"],
            },
            {
                "trigger_action": "Wholesale obligation means competitors benefit from eir's fiber investment",
                "side_effect": "eir builds the network but competitors can resell at regulated prices",
                "attack_vector": "Three and Vodafone offer fiber broadband without network build costs",
                "severity": "high",
                "evidence": ["open eir wholesale provides regulated access to all operators"],
            },
        ],
        "three_ie": [
            {
                "trigger_action": "CK Hutchison evaluating sale of European telecom assets",
                "side_effect": "Ownership uncertainty may limit strategic investment in Ireland",
                "attack_vector": "eir and Vodafone invest while Three faces strategic limbo",
                "severity": "high",
                "evidence": ["CK Hutchison exploring sale of European telecom portfolio"],
            },
            {
                "trigger_action": "No owned fixed broadband infrastructure",
                "side_effect": "Cannot offer competitive converged bundles without wholesale dependency",
                "attack_vector": "eir leverages fixed-mobile convergence advantage",
                "severity": "medium",
                "evidence": ["Three Ireland relies on eir wholesale for fixed broadband"],
            },
        ],
        "vodafone_ie": [
            {
                "trigger_action": "Vodafone Group divesting markets — Ireland could be next",
                "side_effect": "Strategic uncertainty following Vodafone Italia sale",
                "attack_vector": "eir and Three position as committed long-term Irish operators",
                "severity": "medium",
                "evidence": ["Vodafone sold Italian operations to Swisscom Jan 2025"],
            },
            {
                "trigger_action": "Declining mobile market share vs Three's dominance",
                "side_effect": "Subscriber base eroding in competitive mobile market",
                "attack_vector": "Three's aggressive AYCE data plans attract switchers",
                "severity": "medium",
                "evidence": ["Vodafone Ireland ~29% mobile share, trending down"],
            },
        ],
    },

    operator_network_enrichments={
        "eir_ie": {
            "controlled_vs_resale": "Fully owned mobile + fixed network. Ireland's national fixed-line incumbent. 2.2M premises passed with FTTH/FTTC (95% of Ireland). ~100% own-network across mobile and fixed.",
            "evolution_strategy": "FTTH expansion to near-universal coverage. 5G standalone rollout. Legacy copper retirement. Wholesale revenue growth as competitors use open eir. NJJ operational efficiency.",
            "consumer_impact": "Fastest fiber speeds in Ireland. eir Fibre + eir Mobile convergent bundles. Premium brand positioning. Best rural coverage via own fixed network.",
            "b2b_impact": "Growing enterprise ICT provider. Fiber and connectivity for multinationals (Ireland is EU tech hub). Managed services. Government contracts.",
            "cost_impact": "FTTH capex elevated but declining per-homepass as rollout matures. Wholesale revenue offsets build costs. NJJ driving operational efficiency. ~5,000 employees.",
            "org_culture": "Incumbent transforming under NJJ ownership. More agile since Niel took control. Investment-focused. Customer satisfaction improving.",
        },
        "three_ie": {
            "controlled_vs_resale": "Fully owned mobile network. No owned fixed infrastructure; wholesale fiber access via eir. ~100% mobile own-network, 0% fixed own-network.",
            "evolution_strategy": "5G expansion and leadership. Fixed broadband via wholesale. Cost optimization. Potential strategic changes under CK Hutchison review.",
            "consumer_impact": "Ireland's most popular mobile operator. AYCE unlimited data plans. Strong prepaid offering. Growing fixed broadband via wholesale.",
            "b2b_impact": "Three Business for SME segment. Limited large enterprise capability. Mobile-focused B2B.",
            "cost_impact": "Lean mobile-only cost structure. No fixed network capex. CK Hutchison cost discipline. Efficient operations.",
            "org_culture": "Mobile-first culture. Aggressive commercial approach. CK Hutchison management style. Innovation in mobile data pricing.",
        },
        "vodafone_ie": {
            "controlled_vs_resale": "Fully owned mobile network. SIRO JV (50% with ESB) for fiber. ~100% mobile own-network, ~30% fixed via SIRO, 70% wholesale.",
            "evolution_strategy": "5G mobile expansion. SIRO fiber rollout to 770K+ premises. Convergent strategy leveraging mobile + SIRO fiber. Enterprise growth.",
            "consumer_impact": "Premium mobile quality perception. Growing fiber broadband via SIRO. Convergent bundles. Vodafone brand trust.",
            "b2b_impact": "Strong enterprise presence leveraging Vodafone Group. IoT, cloud, managed services. Multinational corporate accounts.",
            "cost_impact": "Vodafone Group procurement advantages. SIRO shared capex. Moderate cost structure. Efficient mobile operations.",
            "org_culture": "Vodafone Group culture. Quality-focused. Professional management. Global perspective.",
        },
    },

    competitive_landscape_notes=[
        "3-player mobile market: Three Ireland (#1 mobile ~48%), Vodafone Ireland (#2 ~29%), eir (#3 ~23%)",
        "eir is the fixed-line infrastructure owner — all operators depend on eir wholesale for broadband",
        "Three Ireland dominant in mobile with AYCE unlimited data strategy",
        "Virgin Media Ireland (Liberty Global) provides cable competition in urban areas",
        "SIRO (ESB/Vodafone JV) building alternative fiber network to 770K+ premises",
        "National Broadband Plan (NBP) addressing rural connectivity gap",
        "5G deployed by all three operators; coverage expanding from Dublin/Cork",
        "CK Hutchison strategic review creates uncertainty for Three Ireland's future",
    ],

    pest_context={
        "political": [
            "ComReg pro-competition regulation; wholesale access mandates on eir",
            "National Broadband Plan (NBP) — EUR 2.7B state-funded rural broadband",
            "Ireland as EU tech hub (Apple, Google, Meta HQs) drives connectivity demand",
            "EU Digital Decade targets applicable",
            "5G spectrum: multi-band auction completed 2023",
        ],
        "economic": [
            "GDP per capita ~EUR 90,000 (nominal, inflated by multinational accounting)",
            "Modified GNI (GNI*) per capita ~EUR 50,000 — better measure of domestic economy",
            "GDP growth ~5% (2024, headline); domestic demand growth ~2-3%",
            "Inflation ~2.5% (2024)",
            "Strong employment; tech sector concentrated in Dublin/Cork",
        ],
        "social": [
            "Population ~5.15M; fastest-growing in EU (immigration-driven)",
            "Smartphone penetration ~90%+",
            "Young demographics vs EU average",
            "Strong rural communities with connectivity needs",
            "Remote work culture well-established since COVID",
        ],
        "technological": [
            "5G rollout by all three operators; coverage concentrated in urban areas",
            "Fiber FTTH coverage ~70% of premises (eir + SIRO)",
            "NBP targeting 100% broadband coverage by 2027",
            "Ireland hosts major EU data centers (Dublin is EU data center hub)",
            "IoT and smart agriculture growing in rural Ireland",
        ],
    },
)
