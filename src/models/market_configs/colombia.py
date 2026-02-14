"""Colombia telecom market configuration."""

from src.models.market_config import MarketConfig

COLOMBIA_CONFIG = MarketConfig(
    market_id="colombia",
    market_name="Colombia",
    country="Colombia",
    currency="COP",
    currency_symbol="$",
    regulatory_body="CRC (Comision de Regulacion de Comunicaciones)",
    population_k=52000,

    customer_segments=[
        {
            "segment_name": "Consumer Prepaid Mass",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable data plans for low-income users",
                "Rural and semi-urban coverage",
            ],
            "pain_points": [
                "Data runs out quickly",
                "Network congestion in Bogota/Medellin",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Social media bundles",
                "Recharge convenience",
            ],
        },
        {
            "segment_name": "Consumer Postpaid & Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "High-quality convergent bundles (mobile+fiber+TV)",
                "5G-ready plans",
            ],
            "pain_points": [
                "Slow fiber rollout outside major cities",
                "Complex pricing structures",
            ],
            "purchase_decision_factors": [
                "Bundle value",
                "Network speed",
                "Device offers",
                "Brand trust",
            ],
        },
        {
            "segment_name": "Enterprise Large",
            "segment_type": "enterprise",
            "unmet_needs": [
                "SD-WAN and multi-cloud connectivity",
                "IoT solutions for agriculture and logistics",
            ],
            "pain_points": [
                "Limited nationwide enterprise coverage",
                "Complex procurement processes",
            ],
            "purchase_decision_factors": [
                "National coverage",
                "SLA guarantees",
                "Managed services capability",
            ],
        },
        {
            "segment_name": "Enterprise SME",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Simple all-in-one business connectivity",
                "Affordable cloud solutions",
            ],
            "pain_points": [
                "High costs for business-grade internet",
                "Poor B2B customer service",
            ],
            "purchase_decision_factors": [
                "Price",
                "Simplicity",
                "Reliability",
            ],
        },
    ],

    operator_bmc_enrichments={
        "tigo_colombia": {
            "key_resources": ["HFC cable network from UNE acquisition", "Largest cable TV base in Colombia", "Strong fiber expansion"],
            "value_propositions": ["Convergent mobile+cable+TV bundles", "Fixed broadband up to 600 Mbps via HFC/fiber"],
            "key_partners": ["EPM (50% JV partner)", "Millicom group shared services"],
            "key_activities": ["Fiber-to-the-home deployment", "5G network rollout", "Enterprise cloud solutions"],
        },
        "claro_co": {
            "key_resources": ["Largest mobile subscriber base", "Widest 4G/5G coverage", "Extensive fiber network"],
            "value_propositions": ["Best network coverage nationwide", "Premium device availability", "Full enterprise portfolio"],
            "key_partners": ["America Movil group", "Enterprise technology partners"],
        },
        "movistar_co": {
            "key_resources": ["Telefonica Group technology platform", "Established enterprise customer base"],
            "value_propositions": ["Competitive postpaid plans", "Enterprise managed services"],
            "key_partners": ["Telefonica Group", "Azure/cloud partnerships"],
        },
        "wom_co": {
            "key_resources": ["Modern 4G network", "Spectrum holdings"],
            "value_propositions": ["Lowest mobile prices in Colombia", "Digital-first customer experience"],
            "key_activities": ["Aggressive subscriber acquisition", "Network coverage expansion"],
        },
    },

    operator_exposures={
        "tigo_colombia": [
            {
                "trigger_action": "WOM aggressive pricing disrupting postpaid economics",
                "side_effect": "ARPU pressure as WOM grows from 2.5M to 4.6M subscribers",
                "attack_vector": "WOM offers 50-70% cheaper plans targeting Tigo's prepaid base",
                "severity": "high",
                "evidence": ["WOM fastest-growing operator in Colombia", "4.6M subs in 3 years"],
            },
            {
                "trigger_action": "50% JV structure with EPM limits strategic flexibility",
                "side_effect": "Slower decision-making and capex allocation vs fully-owned subsidiaries",
                "attack_vector": "Claro moves faster with 100% ownership and larger scale",
                "severity": "medium",
                "evidence": ["JV governance requires EPM alignment on investment decisions"],
            },
            {
                "trigger_action": "Cable network aging while competitors deploy fiber",
                "side_effect": "Speed and perception gap vs Claro fiber offerings",
                "attack_vector": "Claro marketing fiber superiority over cable",
                "severity": "medium",
                "evidence": ["Claro fiber homepass 8M vs Tigo 4.5M"],
            },
        ],
        "claro_co": [
            {
                "trigger_action": "Asymmetric regulatory burden as dominant operator",
                "side_effect": "Higher compliance costs and spectrum allocation restrictions",
                "attack_vector": "CRC pro-competition measures limit Claro's market power",
                "severity": "medium",
                "evidence": ["CRC monitoring market concentration", "Spectrum caps applied"],
            },
        ],
        "movistar_co": [
            {
                "trigger_action": "Telefonica reducing LATAM presence and investment",
                "side_effect": "Underinvestment in network relative to competitors",
                "attack_vector": "Tigo and Claro outspend on 5G and fiber",
                "severity": "high",
                "evidence": ["Telefonica selling non-core LATAM assets"],
            },
        ],
        "wom_co": [
            {
                "trigger_action": "Unsustainable losses while building subscriber base",
                "side_effect": "Potential funding crisis or forced sale if losses continue",
                "attack_vector": "Incumbent operators can sustain pricing war longer than WOM",
                "severity": "high",
                "evidence": ["Negative EBITDA for 3+ years", "Heavy capex on network buildout"],
            },
        ],
    },

    operator_network_enrichments={
        "tigo_colombia": {
            "controlled_vs_resale": "Fully owned HFC cable network (5.2M homes passed) + expanding fiber (4.5M HP) + mobile 4G/5G network. ~92% self-built infrastructure.",
            "evolution_strategy": "FTTH expansion targeting 6M homes by 2027; 5G launch in Bogota/Medellin 2025; HFC DOCSIS 3.1 upgrade for 1 Gbps; cable-to-fiber migration program.",
            "consumer_impact": "Strongest convergent proposition in market (mobile+cable+TV); broadband up to 600 Mbps; cable TV market leader; 5G launching for premium segment.",
            "b2b_impact": "Growing enterprise cloud and connectivity via Millicom/EPM capabilities; data center services; IoT for industrial/agri sectors; Tigo Business brand.",
            "cost_impact": "Dual HFC+fiber investment pressure; JV structure shares capex burden with EPM; high capex ratio (~20% of revenue); cable maintenance costs.",
            "org_culture": "JV culture blending Millicom commercial agility with EPM public utility stability; innovation-oriented with digital transformation focus; strong local brand.",
        },
        "claro_co": {
            "controlled_vs_resale": "Largest integrated network in Colombia — owns mobile (5G leader) + fixed fiber (8M HP) + some cable. ~97% self-built.",
            "evolution_strategy": "5G SA leader with 10% coverage; aggressive FTTH expansion; fiber-first strategy; shutting down 3G by 2027.",
            "consumer_impact": "Best national coverage; 5G pioneer; fastest broadband speeds; premium pricing positions; MagentaEINS-style convergence.",
            "b2b_impact": "Strongest enterprise capabilities — full IT/cloud/security stack; private 5G networks; data centers; government contracts.",
            "cost_impact": "Highest absolute capex but scale-driven efficiency; fiber investment partially offset by copper retirement; strong cash flow supports investment.",
            "org_culture": "America Movil performance culture; aggressive commercial execution; technology leadership ambition; scale-driven efficiency mindset.",
        },
        "movistar_co": {
            "controlled_vs_resale": "Own mobile 4G network + selective fiber deployment (3.5M HP). ~80% own-network, some fixed wholesale dependency.",
            "evolution_strategy": "Selective 5G deployment; fiber expansion in top 5 cities only; efficiency-focused investment; possible market rationalization.",
            "consumer_impact": "Good urban coverage; competitive pricing; limited rural reach; perception gap vs Claro on 5G.",
            "b2b_impact": "Enterprise segment via Telefonica Tech; managed services; limited by reduced investment vs competitors.",
            "cost_impact": "Telefonica efficiency programs reducing opex; selective capex constrains network competitiveness; asset-lighter strategy.",
            "org_culture": "Telefonica Group transformation culture; efficiency-driven; uncertain long-term LATAM commitment affects morale.",
        },
        "wom_co": {
            "controlled_vs_resale": "Building own 4G mobile network; currently ~45% own coverage, ~55% national roaming. No fixed infrastructure.",
            "evolution_strategy": "Rapid 4G site rollout targeting 60% own-coverage by 2026; no fixed network plans; mobile-only strategy.",
            "consumer_impact": "Lowest prices in market; digital-first experience; network quality improving but still perception gap; no convergent bundle.",
            "b2b_impact": "No enterprise presence; focused exclusively on consumer mobile segment.",
            "cost_impact": "Very high capex ratio (34-43% of revenue) for network buildout; national roaming fees as significant opex; loss-making as building scale.",
            "org_culture": "Disruptor/challenger DNA; startup-like agility; aggressive commercial tactics; high employee turnover; investor pressure on path to profitability.",
        },
    },

    competitive_landscape_notes=[
        "4-player market: Claro (leader), Movistar, Tigo, WOM (new entrant)",
        "Claro dominant with ~50% mobile share",
        "Tigo strong in cable TV and broadband via UNE acquisition",
        "WOM disrupting with aggressive pricing since 2020",
        "Active regulator (CRC) promoting competition",
        "Largest addressable market for Millicom in LATAM",
    ],

    pest_context={
        "political": [
            "CRC promoting infrastructure sharing",
            "Government MinTIC digital transformation agenda",
            "Spectrum auctions for 5G planned",
        ],
        "economic": [
            "GDP growth ~3.0%, second largest economy in LATAM after Brazil/Mexico",
            "Peso depreciation impacting equipment costs",
            "Growing middle class driving digital services demand",
        ],
        "social": [
            "52 million population, highly urbanized",
            "Strong social media and streaming adoption",
            "Digital divide between urban and rural areas",
        ],
        "technological": [
            "4G LTE covers ~90% of urban population",
            "5G trials underway, commercial launch expected soon",
            "Fiber broadband expanding rapidly in major cities",
            "Cable HFC infrastructure from Tigo-UNE merger",
        ],
    },
)
