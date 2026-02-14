"""Netherlands telecom market configuration."""

from src.models.market_config import MarketConfig

NETHERLANDS_CONFIG = MarketConfig(
    market_id="netherlands",
    market_name="Netherlands",
    country="Netherlands",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="ACM (Autoriteit Consument & Markt)",
    population_k=17800,

    customer_segments=[
        {
            "segment_name": "Consumer Premium",
            "segment_type": "consumer",
            "unmet_needs": [
                "Seamless converged fixed-mobile bundles",
                "Ultra-reliable 5G standalone connectivity",
            ],
            "pain_points": [
                "Complex multi-provider setups for home + mobile",
                "Limited 5G standalone use cases",
            ],
            "purchase_decision_factors": [
                "Network quality",
                "Bundle integration",
                "5G availability",
                "Brand trust",
            ],
        },
        {
            "segment_name": "Consumer Mainstream",
            "segment_type": "consumer",
            "unmet_needs": [
                "Better value-for-money unlimited data plans",
                "Transparent pricing without hidden costs",
            ],
            "pain_points": [
                "Price increases during contract period",
                "Difficulty comparing plans across operators",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "Network coverage",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable SIM-only plans",
                "No-frills connectivity",
            ],
            "pain_points": [
                "Annual price indexation clauses",
                "Limited MVNO network quality",
            ],
            "purchase_decision_factors": [
                "Lowest monthly price",
                "No contract lock-in",
                "Adequate data",
            ],
        },
        {
            "segment_name": "Enterprise & SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Private 5G network solutions",
                "SD-WAN and cloud connectivity",
                "IoT platform integration",
            ],
            "pain_points": [
                "Complexity of multi-site connectivity",
                "Vendor lock-in concerns",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "Managed services capability",
                "Local support",
                "Price competitiveness",
            ],
        },
    ],

    operator_bmc_enrichments={
        "odido_nl": {
            "key_resources": [
                "Comprehensive 5G mobile network (nationwide coverage)",
                "Spectrum portfolio: 700/800/900/1800/2100/2600/3500 MHz",
                "Strong digital-first brand repositioned in 2023",
            ],
            "value_propositions": [
                "Leading 5G network quality and coverage",
                "Digital-first customer experience",
                "Flexible contract-free plans",
                "Growing fixed-wireless access portfolio",
            ],
            "key_partners": [
                "Ericsson (RAN vendor)",
                "Open Dutch Fiber (fiber access)",
                "Apax Partners / Warburg Pincus (ownership)",
            ],
            "key_activities": [
                "5G network densification and standalone migration",
                "Brand building post-rebrand from T-Mobile",
                "Fixed-wireless access expansion",
                "Enterprise solutions growth",
            ],
        },
        "kpn_nl": {
            "key_resources": [
                "Largest fixed fiber network in NL (4M+ homepass)",
                "Incumbent spectrum portfolio (all major bands)",
                "Premium brand and largest enterprise customer base",
            ],
            "value_propositions": [
                "Convergent quad-play (mobile+broadband+TV+fixed line)",
                "Netherlands' most extensive fiber network",
                "Premium network quality and reliability",
                "Leading enterprise ICT solutions provider",
            ],
            "key_partners": [
                "Nokia (5G RAN)",
                "Glaspoort JV (fiber open access)",
                "Microsoft Azure (cloud partnership)",
            ],
            "key_activities": [
                "Accelerated FTTH rollout (target 80%+ 2027)",
                "Copper network retirement",
                "Enterprise cloud and security services",
                "Operational efficiency and cost reduction",
            ],
        },
        "vodafoneziggo_nl": {
            "key_resources": [
                "Largest cable/HFC network (7M+ homepass DOCSIS 3.1)",
                "Combined Vodafone mobile + Ziggo fixed infrastructure",
                "Entertainment content portfolio (Ziggo Sport, ESPN)",
            ],
            "value_propositions": [
                "Full convergent bundles (cable broadband + mobile)",
                "Gigabit broadband via DOCSIS 3.1 upgrade",
                "Comprehensive entertainment and sports content",
                "Competitive family and multi-SIM plans",
            ],
            "key_partners": [
                "Liberty Global (JV co-owner, technology sharing)",
                "Vodafone Group (JV co-owner, brand)",
            ],
            "key_activities": [
                "DOCSIS 3.1 to DOCSIS 4.0 upgrade path",
                "Network convergence (mobile + cable)",
                "Fiber overbuild in key areas",
                "B2B growth leveraging combined infrastructure",
            ],
        },
    },

    operator_exposures={
        "odido_nl": [
            {
                "trigger_action": "Brand rebrand from established T-Mobile to new Odido brand",
                "side_effect": "Customer confusion and potential churn during brand transition",
                "attack_vector": "KPN and VodafoneZiggo target Odido switchers with competitive offers",
                "severity": "medium",
                "evidence": ["Rebranded September 2023, still building brand awareness"],
            },
            {
                "trigger_action": "No owned fixed broadband infrastructure",
                "side_effect": "Cannot offer true converged bundles without wholesale access",
                "attack_vector": "KPN and VodafoneZiggo leverage convergence advantage",
                "severity": "high",
                "evidence": ["Relies on fixed-wireless access and wholesale fiber for broadband"],
            },
            {
                "trigger_action": "Ownership transition from Deutsche Telekom to PE consortium",
                "side_effect": "Potential underinvestment risk under PE ownership model",
                "attack_vector": "Competitors invest aggressively in network while PE focuses on returns",
                "severity": "medium",
                "evidence": ["Apax/Warburg Pincus acquisition completed 2024"],
            },
        ],
        "kpn_nl": [
            {
                "trigger_action": "Aggressive fiber investment commitments (multi-billion EUR program)",
                "side_effect": "Elevated capex pressure on free cash flow",
                "attack_vector": "VodafoneZiggo already has nationwide broadband via cable",
                "severity": "medium",
                "evidence": ["KPN accelerating FTTH rollout, target 80% by 2027"],
            },
            {
                "trigger_action": "Legacy copper network retirement",
                "side_effect": "Customer disruption and migration costs",
                "attack_vector": "Competitors target KPN copper customers during forced migration",
                "severity": "low",
                "evidence": ["Copper switch-off accelerating in fiber-covered areas"],
            },
        ],
        "vodafoneziggo_nl": [
            {
                "trigger_action": "Vodafone Group evaluating strategic options for JV stake",
                "side_effect": "Ownership uncertainty affects strategic planning",
                "attack_vector": "KPN and Odido capitalize on VodafoneZiggo uncertainty",
                "severity": "high",
                "evidence": ["Vodafone Group portfolio review; Liberty Global deleveraging"],
            },
            {
                "trigger_action": "Cable technology evolution path (DOCSIS 4.0) vs fiber",
                "side_effect": "Risk of technology perception gap vs FTTH players",
                "attack_vector": "KPN markets fiber as superior future-proof technology",
                "severity": "medium",
                "evidence": ["Fiber marketing emphasizes symmetrical speeds vs cable asymmetric"],
            },
        ],
    },

    operator_network_enrichments={
        "odido_nl": {
            "controlled_vs_resale": "Fully owned mobile network with nationwide 5G/4G coverage. No owned fixed infrastructure; uses fixed-wireless access (FWA) and wholesale fiber via Open Dutch Fiber for broadband. ~100% mobile own-network.",
            "evolution_strategy": "5G standalone deployment; densification with 3.5 GHz small cells; FWA as fixed broadband alternative; exploring fiber wholesale partnerships. Target: #1 mobile network quality.",
            "consumer_impact": "Strongest 5G mobile experience; innovative digital-first plans; growing FWA broadband proposition competitive on speed but not on latency vs fiber.",
            "b2b_impact": "Growing enterprise mobile fleet solutions; 5G private networks for manufacturing and logistics; IoT via NarrowBand-IoT and LTE-M.",
            "cost_impact": "Lean opex structure post-separation from DT; PE ownership drives efficiency focus; no legacy fixed network to maintain.",
            "org_culture": "Entrepreneurial post-rebrand culture; digital-first and agile; PE-backed focus on performance and profitability.",
        },
        "kpn_nl": {
            "controlled_vs_resale": "Fully owned mobile + fixed network infrastructure. Largest fiber network (4M+ homepass, expanding to 6M+). Legacy copper being retired. ~95% own-network.",
            "evolution_strategy": "Accelerated FTTH rollout via Glaspoort JV; 5G standalone with Nokia; copper retirement by 2028; converged network architecture; edge computing rollout.",
            "consumer_impact": "Highest reliability perception; premium converged bundles; best fiber broadband speeds; widest TV content via KPN iTV.",
            "b2b_impact": "Leading enterprise ICT provider; SD-WAN, cloud connectivity, managed security; public sector contracts; data center services.",
            "cost_impact": "Fiber rollout capex elevated but declining per-homepass cost; copper retirement saves opex long-term; operational simplification program.",
            "org_culture": "Traditional incumbent evolving to agile; strong engineering culture; ESG leader; customer satisfaction focus.",
        },
        "vodafoneziggo_nl": {
            "controlled_vs_resale": "Combined cable HFC (7M+ homepass, DOCSIS 3.1) + mobile network. JV structure gives full infrastructure control. ~90% own-network (some mobile RAN sharing).",
            "evolution_strategy": "DOCSIS 3.1→4.0 upgrade; selective fiber overbuild; 5G rollout leveraging Vodafone Group technology; converged core network modernization.",
            "consumer_impact": "Best broadband value via cable gigabit; strong entertainment bundle (Ziggo Sport, Disney+); comprehensive family plans with multi-SIM.",
            "b2b_impact": "Combined fixed-mobile enterprise offering; cloud and IoT via Vodafone Business; cable-based business broadband.",
            "cost_impact": "JV synergies from combined operations; cable upgrade cheaper than greenfield fiber; mobile network sharing opportunities.",
            "org_culture": "Dual-parent JV culture; strong commercial execution; entertainment-focused; customer retention emphasis.",
        },
    },

    competitive_landscape_notes=[
        "3-player market (KPN, VodafoneZiggo, Odido) with active MVNO segment",
        "Highly mature market with near-100% mobile penetration",
        "Fixed broadband: KPN fiber vs VodafoneZiggo cable vs Odido FWA",
        "Fiber rollout accelerating with multiple infrastructure players",
        "ACM actively promoting competition and infrastructure access",
        "5G deployed by all three operators; standalone emerging",
        "Convergence a key battleground: fixed-mobile bundles",
    ],

    pest_context={
        "political": [
            "ACM pro-competition regulation; wholesale access mandates",
            "Dutch government Gigabit strategy targeting full coverage by 2030",
            "EU Digital Decade goals shaping national policy",
            "Spectrum policy: 3.5 GHz auction completed 2023",
        ],
        "economic": [
            "GDP per capita ~EUR 52,000; high purchasing power",
            "GDP growth ~1.5-2.0%; stable mature economy",
            "Inflation normalizing to ~2-3% after 2022-23 spike",
            "Labor market tight; telecom talent competition",
        ],
        "social": [
            "Population ~17.8M; aging demographics",
            "Very high smartphone penetration (~95%)",
            "Strong digital literacy and e-commerce adoption",
            "Growing remote/hybrid work driving broadband demand",
        ],
        "technological": [
            "5G rollout by all operators; standalone deployment 2025+",
            "Fiber-to-the-home rollout accelerating (KPN + Glaspoort + open access players)",
            "DOCSIS 3.1 deployed on VodafoneZiggo cable; 4.0 planned",
            "IoT and private 5G enterprise use cases growing",
            "Open RAN trials underway",
        ],
    },
)
