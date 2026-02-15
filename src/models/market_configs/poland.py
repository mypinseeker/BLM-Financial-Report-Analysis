"""Poland telecom market configuration."""

from src.models.market_config import MarketConfig

POLAND_CONFIG = MarketConfig(
    market_id="poland",
    market_name="Poland",
    country="Poland",
    currency="PLN",
    currency_symbol="z\u0142",
    regulatory_body="UKE (Urz\u0105d Komunikacji Elektronicznej)",
    population_k=37750,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "True quad-play convergence (mobile + broadband + TV + fixed line)",
                "Reliable fiber broadband across smaller cities and rural areas",
            ],
            "pain_points": [
                "Limited fiber availability outside major cities",
                "Complex bundle structures with different lock-in periods",
            ],
            "purchase_decision_factors": [
                "Network quality and coverage",
                "Bundle value and convenience",
                "TV content (sports, entertainment)",
                "Brand trust",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better mobile data allowances at competitive prices",
                "Affordable unlimited mobile plans",
            ],
            "pain_points": [
                "Price-to-quality ratio still unfavorable vs Western Europe",
                "Annual price increases embedded in contracts",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data volume",
                "Network coverage",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive / Prepaid",
            "segment_type": "consumer",
            "unmet_needs": [
                "Low-cost prepaid connectivity",
                "Flexible no-contract plans",
            ],
            "pain_points": [
                "Prepaid data allowances still limited vs postpaid",
                "MVNOs have inconsistent network quality",
            ],
            "purchase_decision_factors": [
                "Lowest price",
                "No contract commitment",
                "Adequate coverage",
            ],
        },
        {
            "segment_name": "Enterprise & Government",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Private 5G networks for manufacturing and logistics",
                "Cloud and cybersecurity managed services",
                "IoT solutions for smart cities and agriculture",
            ],
            "pain_points": [
                "Limited enterprise-grade fiber connectivity outside Warsaw",
                "Complex procurement processes for government contracts",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "National coverage",
                "Managed services capability",
                "Price competitiveness",
            ],
        },
    ],

    operator_bmc_enrichments={
        "play_pl": {
            "key_resources": [
                "Poland's largest mobile subscriber base (~15M+ subscribers)",
                "Modern 5G/4G network (Iliad Group investment since 2020)",
                "Strong consumer brand (\"Play\" recognized as innovative and value-driven)",
                "Iliad Group technology platform and procurement synergies",
            ],
            "value_propositions": [
                "Poland's #1 mobile operator by subscribers",
                "Competitive unlimited mobile plans (PLAY, Virgin Mobile sub-brand)",
                "Growing 5G coverage and network quality",
                "Digital-first customer experience",
            ],
            "key_partners": [
                "Nokia and Ericsson (dual-vendor 5G RAN)",
                "Iliad Group (parent company, technology sharing)",
                "Orange Polska (fiber wholesale access for fixed broadband)",
            ],
            "key_activities": [
                "5G network rollout and densification",
                "Fixed broadband development via fiber partnerships",
                "Enterprise/B2B segment growth",
                "Cost optimization leveraging Iliad Group synergies",
            ],
        },
        "orange_pl": {
            "key_resources": [
                "Largest fiber network in Poland (5M+ FTTH homepass)",
                "Comprehensive mobile + fixed convergent network",
                "Premium brand and largest enterprise customer base",
                "Orange Group technology and procurement support",
            ],
            "value_propositions": [
                "Poland's leading convergent operator (fiber + mobile)",
                "Premium network quality across fixed and mobile",
                "Comprehensive enterprise ICT solutions",
                "Orange Love convergent bundles",
            ],
            "key_partners": [
                "Orange Group (parent company, technology sharing)",
                "Nokia (5G RAN vendor)",
                "Microsoft (cloud and enterprise services)",
            ],
            "key_activities": [
                "Accelerated fiber FTTH rollout",
                "5G standalone deployment",
                "Enterprise digital transformation services",
                "Convergent bundle growth (Orange Love)",
            ],
        },
        "tmobile_pl": {
            "key_resources": [
                "Comprehensive 5G/4G mobile network (DT investment)",
                "Growing fixed broadband via Deutsche Telekom fiber partnerships",
                "Strong T-Mobile brand backed by Deutsche Telekom",
                "Magenta TV content platform",
            ],
            "value_propositions": [
                "5G network leadership in Poland",
                "Competitive mobile and convergent plans",
                "T-Mobile brand quality and trust",
                "Growing fixed broadband via fiber and FWA",
            ],
            "key_partners": [
                "Deutsche Telekom (parent company)",
                "Ericsson (RAN vendor)",
                "Netflix, HBO (content partnerships)",
            ],
            "key_activities": [
                "5G network expansion and leadership positioning",
                "Fixed broadband growth via fiber access and FWA",
                "Convergent bundle development",
                "Enterprise segment growth",
            ],
        },
        "plus_pl": {
            "key_resources": [
                "Comprehensive mobile + fixed network",
                "Cyfrowy Polsat media empire (Polsat TV, IPLA, Polsat Sport)",
                "Convergent media-telecom platform unique in Poland",
                "Extensive retail distribution (Polkomtel + Polsat stores)",
            ],
            "value_propositions": [
                "Unique media-telecom convergence (TV + mobile + broadband)",
                "Polsat Sport exclusive content (sports rights)",
                "Comprehensive quad-play bundles",
                "Strong regional presence and distribution",
            ],
            "key_partners": [
                "Cyfrowy Polsat (parent conglomerate)",
                "Huawei and Nokia (RAN vendors)",
                "Netia (fixed broadband subsidiary)",
            ],
            "key_activities": [
                "Media-telecom convergence strategy",
                "5G network rollout",
                "Fixed broadband expansion via Netia",
                "Content acquisition and sports rights",
            ],
        },
    },

    operator_exposures={
        "play_pl": [
            {
                "trigger_action": "No owned fixed broadband infrastructure",
                "side_effect": "Cannot offer true converged bundles without wholesale dependency",
                "attack_vector": "Orange Polska and Plus leverage convergent advantage",
                "severity": "high",
                "evidence": ["Play relies on wholesale fiber access; no cable or fiber network of its own"],
            },
            {
                "trigger_action": "Iliad Group managing 3 markets (France, Italy, Poland) with different dynamics",
                "side_effect": "Capital allocation competition between markets",
                "attack_vector": "DT (T-Mobile) and Orange Group can dedicate more resources to Poland",
                "severity": "medium",
                "evidence": ["Iliad Group capex split across France, Italy, Poland"],
            },
        ],
        "orange_pl": [
            {
                "trigger_action": "Massive fiber investment program requires sustained capex",
                "side_effect": "Elevated capex constraining free cash flow",
                "attack_vector": "Play offers competitive mobile without fiber investment burden",
                "severity": "medium",
                "evidence": ["Orange Polska targeting 6M+ FTTH homepass by 2026"],
            },
            {
                "trigger_action": "Legacy copper retirement creating customer migration friction",
                "side_effect": "Forced migrations can lead to customer churn",
                "attack_vector": "Competitors target Orange copper customers during migration",
                "severity": "low",
                "evidence": ["Copper retirement accelerating in fiber-covered areas"],
            },
        ],
        "tmobile_pl": [
            {
                "trigger_action": "Limited owned fixed broadband infrastructure vs Orange Polska",
                "side_effect": "Convergent offering weaker than Orange's fiber + mobile",
                "attack_vector": "Orange Polska markets fiber as differentiator",
                "severity": "medium",
                "evidence": ["T-Mobile Polska uses FWA and wholesale fiber for broadband"],
            },
            {
                "trigger_action": "Deutsche Telekom prioritizes US (T-Mobile US) and German markets",
                "side_effect": "Poland may receive less strategic attention and investment",
                "attack_vector": "Orange Group and Iliad prioritize their Polish operations more",
                "severity": "low",
                "evidence": ["T-Mobile US is DT's main growth driver; Poland is smaller market"],
            },
        ],
        "plus_pl": [
            {
                "trigger_action": "Cyfrowy Polsat conglomerate complexity and governance concerns",
                "side_effect": "Complex corporate structure may limit strategic agility",
                "attack_vector": "Simpler-structured competitors can move faster",
                "severity": "medium",
                "evidence": ["Zygmunt Solorz family ownership; succession planning concerns"],
            },
            {
                "trigger_action": "Declining linear TV viewing threatens media-telecom convergence model",
                "side_effect": "Key differentiator (Polsat TV content) losing relevance for younger users",
                "attack_vector": "Netflix, Disney+, YouTube compete for attention without telecom bundling",
                "severity": "medium",
                "evidence": ["Linear TV viewership declining; streaming growing"],
            },
        ],
    },

    operator_network_enrichments={
        "play_pl": {
            "controlled_vs_resale": "Fully owned mobile network with nationwide 5G/4G coverage (~98% pop). No owned fixed infrastructure; exploring wholesale fiber access and FWA. ~100% mobile own-network.",
            "evolution_strategy": "5G densification on 3.5 GHz + 700 MHz. Mobile-first strategy evolving toward convergence via fiber partnerships. Iliad Group technology sharing. Cost optimization.",
            "consumer_impact": "Poland's largest mobile subscriber base. Competitive unlimited mobile plans. Growing but limited fixed broadband via wholesale. Virgin Mobile sub-brand for value segment.",
            "b2b_impact": "Growing enterprise mobile fleet management. 5G private networks for enterprise. Limited fixed B2B vs Orange. Play Business expanding.",
            "cost_impact": "Lean cost structure from Iliad Group DNA. No fixed network maintenance costs. Iliad procurement synergies reduce equipment costs. Efficiency improving post-acquisition.",
            "org_culture": "Challenger culture reinforced by Iliad ownership. Dynamic and commercially aggressive. Engineering-focused. Digital-first operations.",
        },
        "orange_pl": {
            "controlled_vs_resale": "Fully owned mobile + fixed network. Largest fiber network (5M+ FTTH homepass, expanding). Legacy copper being retired. ~95% own-network.",
            "evolution_strategy": "Accelerated FTTH rollout targeting 6M+ homepass. 5G standalone on Nokia. Copper retirement. Converged network architecture. Open Fiber co-investment model.",
            "consumer_impact": "Premium convergent operator. Best fiber speeds. Orange Love bundles (mobile+broadband+TV). Widest fixed+mobile coverage.",
            "b2b_impact": "Poland's leading enterprise ICT provider. Cloud, cybersecurity, SD-WAN. Government contracts. Data center services.",
            "cost_impact": "Fiber capex elevated but declining per-homepass. Copper retirement saves opex. Orange Group shared services. Operational simplification.",
            "org_culture": "Incumbent evolving. Orange Group values. Strong engineering culture. Customer satisfaction focus. ESG leadership in Poland.",
        },
        "tmobile_pl": {
            "controlled_vs_resale": "Fully owned mobile network. Limited fixed: FWA + wholesale fiber + small own fiber. ~100% mobile own-network, ~30% fixed via own/FWA, 70% wholesale.",
            "evolution_strategy": "5G leadership strategy. Fixed broadband via FWA and selective fiber build. Deutsche Telekom technology platform. Convergent growth.",
            "consumer_impact": "Strong 5G network perception. Competitive Magenta plans. Growing convergent offering. Content partnerships (Netflix, HBO).",
            "b2b_impact": "T-Mobile Business for enterprise. Growing cloud and connectivity. DT enterprise solutions. Government contracts.",
            "cost_impact": "DT group procurement advantages. Moderate capex profile. Shared technology platforms. Efficient operations.",
            "org_culture": "Deutsche Telekom culture. Quality-focused. Professional management. Structured decision-making.",
        },
        "plus_pl": {
            "controlled_vs_resale": "Fully owned mobile network (Polkomtel) + Netia fixed infrastructure. Cable and fiber via Netia (~2M homepass). ~85% own-network overall.",
            "evolution_strategy": "Media-telecom convergence. 5G rollout. Netia fiber and cable expansion. Content as differentiator. Integrated media+telecom platform.",
            "consumer_impact": "Unique media convergence. Polsat Sport exclusive content. Comprehensive bundles. Strong regional brand presence.",
            "b2b_impact": "Polkomtel Business. Netia enterprise connectivity. Combined mobile+fixed for enterprise. Limited vs Orange in large enterprise.",
            "cost_impact": "Media content costs alongside network capex. Netia fixed costs. Scale advantages from conglomerate. Synergies between media and telecom.",
            "org_culture": "Media-telecom hybrid culture. Entrepreneurial (Solorz family). Content-focused. Commercial agility.",
        },
    },

    competitive_landscape_notes=[
        "4-player mobile market: Play (#1 mobile), Orange Polska (convergent leader), T-Mobile (DT-backed), Plus/Polkomtel (media-telecom)",
        "Convergence growing but Poland still more mobile-centric than Western Europe",
        "Orange Polska leads fixed broadband and fiber; Play is mobile-only champion",
        "Plus/Cyfrowy Polsat unique media-telecom model with Polsat TV integration",
        "5G deployed by all four operators; 3.5 GHz auction completed",
        "Fiber rollout accelerating; Orange leading, government subsidies for rural areas",
        "Active MVNO segment (~10% of mobile market)",
        "UKE promoting infrastructure competition and wholesale access",
    ],

    pest_context={
        "political": [
            "UKE pro-competition regulation; wholesale access mandates",
            "Polish government broadband subsidies for rural areas (EU co-funded)",
            "EU Digital Decade targets driving fiber and 5G investment",
            "5G spectrum: 3.5 GHz auctioned 2024; 700 MHz allocated",
            "Government digital transformation agenda (e-Government)",
        ],
        "economic": [
            "GDP per capita ~EUR 18,000 (PLN 80,000); growing middle-income economy",
            "GDP growth ~3.0-3.5%; among fastest-growing EU economies",
            "Inflation ~3-5% (higher than Western EU)",
            "PLN/EUR exchange rate ~4.3; moderate currency volatility",
            "Strong consumer spending growth",
        ],
        "social": [
            "Population ~37.8M; mild decline, aging demographics",
            "Smartphone penetration ~85%",
            "Growing demand for streaming and digital entertainment",
            "Urbanization trend driving fiber demand in cities",
            "Remote/hybrid work adoption increasing broadband needs",
        ],
        "technological": [
            "5G rollout by all four operators; 3.5 GHz coverage expanding",
            "Fiber FTTH rollout accelerating: Orange leading with 5M+ homepass",
            "Government KPO/NCBR funding for 5G and fiber infrastructure",
            "IoT growing in manufacturing and smart city applications",
            "Cloud adoption accelerating among Polish enterprises",
        ],
    },
)
