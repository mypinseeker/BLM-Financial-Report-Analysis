"""France telecom market configuration."""

from src.models.market_config import MarketConfig

FRANCE_CONFIG = MarketConfig(
    market_id="france",
    market_name="France",
    country="France",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="ARCEP (Autorit\u00e9 de R\u00e9gulation des Communications \u00c9lectroniques, des Postes et de la Distribution de la Presse)",
    population_k=68170,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "Seamless multi-screen entertainment experience (TV, mobile, home)",
                "Ultra-fast symmetric fiber for remote work and gaming",
            ],
            "pain_points": [
                "Complex bundle structures and hidden fees",
                "12-month promotional pricing that jumps significantly",
            ],
            "purchase_decision_factors": [
                "Fiber speed and reliability",
                "TV content offering (sports, cinema)",
                "Bundle value (quad-play)",
                "Brand reputation and customer service",
            ],
        },
        {
            "segment_name": "Consumer Value-Seeking",
            "segment_type": "consumer",
            "unmet_needs": [
                "Transparent low-cost unlimited mobile plans",
                "Affordable fiber broadband without long contracts",
            ],
            "pain_points": [
                "Post-promotional price hikes",
                "Difficulty comparing real costs across operators",
            ],
            "purchase_decision_factors": [
                "Monthly cost (post-promo)",
                "Data volume / unlimited",
                "Network coverage",
                "Contract flexibility (no lock-in)",
            ],
        },
        {
            "segment_name": "Consumer SIM-Only / MVNO",
            "segment_type": "consumer",
            "unmet_needs": [
                "Ultra-low-cost mobile-only connectivity",
                "Flexible prepaid/no-contract options",
            ],
            "pain_points": [
                "MVNOs throttle speeds during congestion",
                "Limited 5G access on sub-brands",
            ],
            "purchase_decision_factors": [
                "Lowest price per GB",
                "No commitment",
                "Adequate network quality",
            ],
        },
        {
            "segment_name": "Enterprise & Public Sector",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Private 5G networks for Industry 4.0",
                "Multi-cloud connectivity and SD-WAN",
                "Cybersecurity managed services",
            ],
            "pain_points": [
                "Complex RFP processes for public sector contracts",
                "Vendor lock-in with legacy infrastructure",
            ],
            "purchase_decision_factors": [
                "Network reliability and SLAs",
                "Managed services capability",
                "National and international coverage",
                "Innovation and R&D capability",
            ],
        },
    ],

    operator_bmc_enrichments={
        "free_fr": {
            "key_resources": [
                "Extensive owned fiber network (FTTH via Group Iliad infrastructure)",
                "5G mobile network (3.5 GHz + 700 MHz nationwide)",
                "Freebox product line (Delta, Pop, Ultra) — premium CPE differentiation",
                "Strong brand loyalty among price-sensitive and tech-savvy customers",
            ],
            "value_propositions": [
                "Disruptive value: premium services at aggressive pricing",
                "Freebox Ultra: WiFi 7, 8Gbps symmetric, integrated NAS and player",
                "Free Mobile: EUR 19.99/month 300GB 5G with Freebox, EUR 15.99 standalone",
                "Transparency: simple pricing, no hidden fees, no price hikes",
            ],
            "key_partners": [
                "Nokia (5G RAN and fiber)",
                "Qualcomm (Freebox chipsets)",
                "Canal+ (TV content partnership)",
            ],
            "key_activities": [
                "Fiber rollout acceleration (targeting 80%+ coverage by 2025)",
                "5G network densification (3.5 GHz urban + 700 MHz rural)",
                "Freebox innovation cycles (hardware + software)",
                "B2B segment development (Free Pro launched 2021)",
            ],
        },
        "orange_fr": {
            "key_resources": [
                "Largest fiber network in France (35M+ FTTH homepass, nationwide)",
                "Comprehensive 5G/4G mobile network with widest rural coverage",
                "Premium brand and largest enterprise/government customer base",
                "Orange Business (global enterprise ICT division)",
            ],
            "value_propositions": [
                "France's most extensive fiber and mobile coverage",
                "Premium converged bundles (Livebox, Open plans)",
                "Leading enterprise cloud, cybersecurity, and IoT solutions",
                "5G innovation leadership and network quality",
            ],
            "key_partners": [
                "Ericsson and Nokia (dual-vendor RAN)",
                "Microsoft Azure (cloud partnership)",
                "Canal+ (exclusive content deals)",
            ],
            "key_activities": [
                "Fiber network expansion and copper retirement",
                "5G standalone deployment and private networks",
                "Enterprise digital transformation services",
                "Cost optimization and operational efficiency (Lead the Future plan)",
            ],
        },
        "sfr_fr": {
            "key_resources": [
                "Comprehensive cable/HFC and fiber network (Numericable legacy + fiber build)",
                "Full 5G/4G mobile network",
                "Altice media assets (BFM TV, RMC, etc.)",
                "SFR brand + RED by SFR (low-cost sub-brand)",
            ],
            "value_propositions": [
                "Convergent bundles leveraging cable + fiber + mobile",
                "RED by SFR: aggressive digital-only value brand",
                "Media convergence (BFM, RMC Sport content)",
                "Competitive enterprise connectivity solutions",
            ],
            "key_partners": [
                "Altice Group (parent company, media integration)",
                "Nokia (5G deployment partner)",
            ],
            "key_activities": [
                "Network quality improvement (historically criticized)",
                "Debt reduction under Altice restructuring",
                "Customer experience recovery post-restructuring",
                "Fiber footprint expansion",
            ],
        },
        "bouygues_telecom_fr": {
            "key_resources": [
                "Growing fiber network (accelerating FTTH build-out)",
                "Competitive 5G/4G mobile network",
                "Bouygues Group synergies (construction, media TF1)",
                "Strong regional brand perception and distribution",
            ],
            "value_propositions": [
                "Best customer satisfaction scores among French operators",
                "Competitive convergent B&You and Sensation bundles",
                "Strong 5G rollout and network quality improvement",
                "B&You: digital-only brand competing with RED by SFR and Free",
            ],
            "key_partners": [
                "Bouygues Group (parent company, TF1 media)",
                "Huawei and Nokia (RAN vendors)",
                "SDAIF (fiber co-investment vehicle)",
            ],
            "key_activities": [
                "Accelerated FTTH deployment (co-investment model)",
                "Mobile network quality improvement (closing gap with Orange)",
                "Convergence strategy (fixed-mobile bundles)",
                "B2B segment growth",
            ],
        },
    },

    operator_exposures={
        "free_fr": [
            {
                "trigger_action": "Aggressive pricing model constrains ARPU growth",
                "side_effect": "Revenue per user significantly below Orange and Bouygues",
                "attack_vector": "Competitors invest more per customer in network quality and content",
                "severity": "medium",
                "evidence": ["Free Mobile ARPU ~EUR 13-14/month vs Orange ~EUR 20+"],
            },
            {
                "trigger_action": "Limited B2B/enterprise presence despite Free Pro launch",
                "side_effect": "Missing large and growing revenue pool in enterprise ICT",
                "attack_vector": "Orange dominates enterprise with Orange Business; SFR and Bouygues growing",
                "severity": "medium",
                "evidence": ["Free Pro launched 2021; still <5% enterprise market share"],
            },
            {
                "trigger_action": "Reliance on price disruption in mature market with decreasing headroom",
                "side_effect": "Limited ability to raise prices without losing brand positioning",
                "attack_vector": "Competitors have converged on competitive pricing; Free's price gap narrowing",
                "severity": "medium",
                "evidence": ["French telecom ARPU among lowest in Western Europe"],
            },
        ],
        "orange_fr": [
            {
                "trigger_action": "Massive fiber and copper retirement investment program",
                "side_effect": "Elevated capex constraining shareholder returns",
                "attack_vector": "Free and Bouygues co-invest in fiber at lower cost per homepass",
                "severity": "medium",
                "evidence": ["Orange France capex ~EUR 3.5B/year; copper retirement by 2030"],
            },
            {
                "trigger_action": "Legacy cost structure from incumbent operations",
                "side_effect": "Higher opex per customer than challenger operators",
                "attack_vector": "Free operates with 60% fewer employees per customer",
                "severity": "medium",
                "evidence": ["Orange France ~75,000 employees vs Free ~17,000"],
            },
        ],
        "sfr_fr": [
            {
                "trigger_action": "Altice Group financial restructuring and debt burden",
                "side_effect": "Underinvestment risk and management distraction",
                "attack_vector": "All competitors outspend SFR on network quality",
                "severity": "high",
                "evidence": ["Altice France debt restructuring 2024-2025; Patrick Drahi stepping back"],
            },
            {
                "trigger_action": "Persistent network quality perception gap",
                "side_effect": "Highest churn rate among big 4 operators",
                "attack_vector": "ARCEP QoS reports consistently rank SFR last on key metrics",
                "severity": "high",
                "evidence": ["SFR losing ~200K mobile subs per quarter in 2024"],
            },
        ],
        "bouygues_telecom_fr": [
            {
                "trigger_action": "Smallest of the big 4 by revenue and subscriber base",
                "side_effect": "Scale disadvantage in content acquisition and spectrum costs",
                "attack_vector": "Orange and Free have larger customer bases to amortize investments",
                "severity": "medium",
                "evidence": ["Bouygues Telecom ~15% mobile market share vs Orange ~35%"],
            },
            {
                "trigger_action": "Failed merger with SFR (2014) leaves organic growth as only path",
                "side_effect": "No transformative M&A option in concentrated French market",
                "attack_vector": "Competitors benefit from scale; Bouygues must grow share organically",
                "severity": "low",
                "evidence": ["French market is 4-player with no M&A opportunities"],
            },
        ],
    },

    operator_network_enrichments={
        "free_fr": {
            "controlled_vs_resale": "Fully owned mobile network (5G/4G/3G). FTTH via Iliad Group fiber build + co-investment in Orange and SFR fiber zones. ~85% own fiber homepass, 15% co-investment access.",
            "evolution_strategy": "5G on 3.5 GHz (urban) + 700 MHz (nationwide) + 2100 MHz (capacity). Aggressive fiber build targeting 37M+ FTTH homepass. Copper migration. Freebox hardware cycles every 2-3 years.",
            "consumer_impact": "Disruptive pricing with premium hardware (Freebox Ultra WiFi 7). Best value-for-money in French market. Growing 5G coverage. Free Ligue 1 football rights via partnership.",
            "b2b_impact": "Free Pro launched 2021 targeting SMEs. Growing fiber business connectivity. Limited large enterprise capability vs Orange. Data center services (Scaleway by Iliad).",
            "cost_impact": "Lean cost structure: ~17,000 employees serving 23M+ mobile + 7M+ fixed subs. Highly automated customer service. Low distribution costs (online-first + Free Centers).",
            "org_culture": "Entrepreneurial and engineering-driven. Xavier Niel's disruptive DNA. Innovation-focused (hardware R&D in-house). Lean organization. Startup mentality at scale.",
        },
        "orange_fr": {
            "controlled_vs_resale": "Fully owned mobile + fixed network. Largest fiber network (35M+ FTTH homepass). Legacy copper being retired (target 2030). ~98% own-network.",
            "evolution_strategy": "Fiber acceleration and copper shutdown. 5G standalone deployment. Network sharing with Free in less-dense areas. Open RAN trials. AI-driven network optimization.",
            "consumer_impact": "Premium network quality perception. Widest coverage (urban + rural). Livebox Fiber up to 8Gbps. Comprehensive TV platform. Premium pricing justified by quality.",
            "b2b_impact": "France's leading enterprise ICT provider via Orange Business. Cloud, cybersecurity, SD-WAN, IoT. Major government contracts. International enterprise connectivity.",
            "cost_impact": "Elevated opex from legacy workforce (civil servant status employees). Copper retirement costs. Scale advantages in procurement. Lead the Future efficiency program.",
            "org_culture": "Incumbent evolving under CEO Christel Heydemann. Engineering excellence. Strong social responsibility (former state company). Complex union relations. ESG leadership.",
        },
        "sfr_fr": {
            "controlled_vs_resale": "Fully owned mobile network + Numericable cable HFC + growing fiber. ~90% own-network. Cable/fiber covers 22M+ premises.",
            "evolution_strategy": "Fiber build leveraging Numericable HFC upgrade path + new FTTH. 5G rollout on 3.5 GHz. Network quality improvement investment. DOCSIS evolution on cable footprint.",
            "consumer_impact": "Competitive pricing via RED by SFR sub-brand. Cable broadband reliability in covered areas. BFM TV and RMC Sport content. Network quality reputation lagging.",
            "b2b_impact": "SFR Business targeting mid-market and enterprise. Cloud and connectivity services. Growing but distant third behind Orange Business.",
            "cost_impact": "Altice cost-cutting legacy. Debt service burden on parent. Leaner workforce than Orange but underinvestment risk. Cable infrastructure provides cost advantage in covered areas.",
            "org_culture": "Turbulent recent history under Altice restructuring. High management turnover. Cost-focused culture. Rebuilding stability post-Drahi era.",
        },
        "bouygues_telecom_fr": {
            "controlled_vs_resale": "Fully owned mobile network. Fiber via co-investment (SDAIF vehicle + Orange co-invest). Growing own FTTH footprint. ~80% own-network for fixed, 100% mobile.",
            "evolution_strategy": "Accelerated fiber build via co-investment model. 5G on 3.5 GHz + 2100 MHz. Network quality improvement (Opensignal awards). Mobile-first evolving to convergent.",
            "consumer_impact": "Best customer satisfaction (JD Power equivalent). Strong B&You brand for value seekers. Growing fiber coverage. Competitive 5G rollout.",
            "b2b_impact": "Bouygues Telecom Entreprises growing in mid-market. Construction sector synergies (Bouygues Group). Smart building solutions. Limited large enterprise vs Orange.",
            "cost_impact": "Co-investment model reduces fiber capex per homepass. Moderate employee base. Bouygues Group shared services. Efficient cost structure.",
            "org_culture": "Customer-first culture reflected in satisfaction scores. Bouygues Group values (innovation, respect). Growing ambition under CEO Benoit Torloting. Pragmatic operator.",
        },
    },

    competitive_landscape_notes=[
        "4-player market: Orange (incumbent), SFR (cable+mobile), Bouygues Telecom (challenger), Free (disruptor)",
        "Free's 2012 mobile launch permanently disrupted pricing; France has among lowest ARPUs in Western Europe",
        "Convergence battle: Orange fiber vs SFR cable vs Bouygues co-invest vs Free own-build",
        "Enterprise market dominated by Orange Business; Free Pro emerging as disruptive challenger",
        "Altice/SFR financial restructuring creating competitive uncertainty",
        "5G deployed by all four operators on 3.5 GHz; coverage expanding rapidly",
        "ARCEP promoting infrastructure competition and co-investment in fiber",
        "Active MVNO segment with ~15% mobile market share (Bouygues/SFR host networks)",
    ],

    pest_context={
        "political": [
            "ARCEP pro-competition regulation; fiber co-investment framework",
            "French state historically influential in telecom (former France Telecom/Orange)",
            "EU Digital Decade targets driving broadband and 5G investment",
            "5G spectrum auction completed 2020 (3.5 GHz), additional bands ongoing",
            "Copper network retirement mandate by 2030",
        ],
        "economic": [
            "GDP per capita ~EUR 40,000; mature high-income economy",
            "GDP growth ~0.8-1.2%; below EU average",
            "Inflation normalizing to ~2-3% after 2022-23 spike",
            "Among lowest telecom ARPUs in Western Europe due to competition",
        ],
        "social": [
            "Population ~68.2M; aging demographics",
            "High smartphone penetration (~90%)",
            "Strong demand for convergent fixed-mobile bundles",
            "Remote/hybrid work adoption driving fiber demand",
            "Growing demand for streaming and gaming bandwidth",
        ],
        "technological": [
            "5G rollout by all four operators; 3.5 GHz coverage expanding 2024-2025",
            "Fiber FTTH rollout: 37M+ premises passed, ~22M active lines",
            "Copper retirement accelerating (ARCEP roadmap to 2030)",
            "IoT and smart city initiatives across major cities",
            "Open RAN trials by Orange and others",
        ],
    },
)
