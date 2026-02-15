"""Cyprus telecom market configuration."""

from src.models.market_config import MarketConfig

CYPRUS_CONFIG = MarketConfig(
    market_id="cyprus",
    market_name="Cyprus",
    country="Cyprus",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="OCECPR (Office of the Commissioner of Electronic Communications and Postal Regulation)",
    population_k=1200,

    customer_segments=[
        {
            "segment_name": "Consumer Urban Connected",
            "segment_type": "consumer",
            "unmet_needs": [
                "Faster and more affordable fiber broadband",
                "Seamless converged fixed-mobile bundles",
            ],
            "pain_points": [
                "Limited competition keeps prices high for a small market",
                "Cyta dominance in fixed broadband limits choice",
            ],
            "purchase_decision_factors": [
                "Network quality and speed",
                "Bundle value (fixed + mobile + TV)",
                "Brand trust",
                "Coverage across the island",
            ],
        },
        {
            "segment_name": "Consumer Price-Sensitive",
            "segment_type": "consumer",
            "unmet_needs": [
                "More affordable unlimited mobile data plans",
                "Transparent pricing without hidden fees",
            ],
            "pain_points": [
                "Small market means less competitive pressure on pricing",
                "Limited MVNO options",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance",
                "Contract flexibility",
                "Prepaid options",
            ],
        },
        {
            "segment_name": "Tourist / Seasonal",
            "segment_type": "consumer",
            "unmet_needs": [
                "Easy tourist SIM activation and eSIM support",
                "Short-term data-heavy plans for visitors",
            ],
            "pain_points": [
                "Cyprus hosts 4M+ tourists annually; seasonal demand spikes",
                "Roaming complexity for non-EU visitors",
            ],
            "purchase_decision_factors": [
                "Ease of purchase",
                "Short-term plan availability",
                "Coverage in tourist areas",
            ],
        },
        {
            "segment_name": "Enterprise & Government",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Managed ICT services for growing Cyprus business sector",
                "Cloud and cybersecurity solutions",
                "Private 5G for shipping/logistics industry",
            ],
            "pain_points": [
                "Cyta dominates enterprise fixed connectivity",
                "Limited scale for advanced managed services",
            ],
            "purchase_decision_factors": [
                "Reliability and SLAs",
                "Price competitiveness",
                "Managed services capability",
                "EU data sovereignty",
            ],
        },
    ],

    operator_bmc_enrichments={
        "epic_cy": {
            "key_resources": [
                "Owned 4G/5G mobile network (launched 5G July 2021)",
                "Growing FTTH fiber network (EIB EUR 19M financing)",
                "Monaco Telecom/NJJ ownership — Xavier Niel telecom expertise",
                "Strong brand in digital-first and young demographics",
            ],
            "value_propositions": [
                "Fastest mobile network in Cyprus (Ookla Speedtest Awards)",
                "Competitive mobile pricing challenging Cyta",
                "5G pioneer in Cyprus market",
                "Growing fiber broadband offering",
            ],
            "key_partners": [
                "Monaco Telecom / NJJ Holding (parent company)",
                "Huawei (network equipment and 5G)",
                "umlaut (network quality assessment)",
                "EIB (FTTH financing)",
            ],
            "key_activities": [
                "5G network expansion toward nationwide coverage",
                "FTTH fiber rollout to compete with Cyta in broadband",
                "Mobile subscriber growth and ARPU improvement",
                "Enterprise segment development",
            ],
        },
        "cyta_cy": {
            "key_resources": [
                "Cyprus fixed-line infrastructure owner (copper + fiber)",
                "Largest mobile subscriber base (~52% market share)",
                "Semi-governmental status — state backing and stability",
                "Vodafone brand partnership for mobile (Cytamobile-Vodafone)",
            ],
            "value_propositions": [
                "Cyprus's #1 operator across all segments",
                "Comprehensive convergent bundles (fixed + mobile + TV)",
                "Nationwide fixed and mobile coverage",
                "Trusted national brand",
            ],
            "key_partners": [
                "Republic of Cyprus (100% state-owned)",
                "Vodafone Group (mobile brand license since 2004)",
                "Nokia/Ericsson (network equipment)",
            ],
            "key_activities": [
                "FTTP fiber rollout (77% coverage achieved)",
                "5G network deployment",
                "Legacy copper network retirement",
                "Digital transformation of public services",
            ],
        },
        "primetel_cy": {
            "key_resources": [
                "Alternative fixed broadband network",
                "Mobile network (smallest of three MNOs)",
                "Established brand in Cyprus market",
            ],
            "value_propositions": [
                "Value-oriented alternative to Cyta",
                "Competitive broadband and TV bundles",
                "Growing mobile offering",
            ],
            "key_partners": [
                "Private ownership (MP Cyprus Holdings)",
                "Equipment vendors for network deployment",
            ],
            "key_activities": [
                "Broadband and TV subscriber growth",
                "Mobile network improvement",
                "Bundle competition against Cyta and Epic",
            ],
        },
    },

    operator_exposures={
        "epic_cy": [
            {
                "trigger_action": "Limited fixed broadband infrastructure vs Cyta's national network",
                "side_effect": "Cannot offer full convergent bundles across Cyprus",
                "attack_vector": "Cyta leverages fixed-mobile convergence advantage",
                "severity": "high",
                "evidence": ["Epic FTTH rollout ongoing but much smaller than Cyta's national copper/fiber network"],
            },
            {
                "trigger_action": "Second-largest mobile operator competing against state-backed Cyta",
                "side_effect": "Scale disadvantage in a small market",
                "attack_vector": "Cyta uses incumbent advantages and state backing",
                "severity": "medium",
                "evidence": ["Epic ~35% mobile share vs Cyta ~52%; small market limits growth"],
            },
        ],
        "cyta_cy": [
            {
                "trigger_action": "Semi-governmental status limits operational agility",
                "side_effect": "Hiring freezes, bureaucratic decision-making",
                "attack_vector": "Epic's private-sector agility and NJJ backing enable faster moves",
                "severity": "medium",
                "evidence": ["Cyta subject to public sector hiring constraints; EUR 148M personnel costs"],
            },
            {
                "trigger_action": "Vodafone brand license dependency for mobile",
                "side_effect": "Mobile brand identity tied to Vodafone Group decisions",
                "attack_vector": "Epic builds independent brand identity",
                "severity": "low",
                "evidence": ["Cytamobile-Vodafone branding depends on Vodafone Group partnership"],
            },
        ],
        "primetel_cy": [
            {
                "trigger_action": "Smallest MNO with limited scale in a small market",
                "side_effect": "Difficulty achieving profitability in mobile",
                "attack_vector": "Epic and Cyta both have larger subscriber bases and more investment",
                "severity": "high",
                "evidence": ["PrimeTel ~13% mobile market share; limited resources vs larger competitors"],
            },
        ],
    },

    operator_network_enrichments={
        "epic_cy": {
            "controlled_vs_resale": "Fully owned mobile network with 4G/5G coverage. Growing FTTH network (EIB EUR 19M financing). ~95% mobile own-network, ~30% fixed via own fiber, rest wholesale.",
            "evolution_strategy": "5G nationwide expansion. FTTH fiber rollout to challenge Cyta in broadband. Mobile-first evolving toward convergence. NJJ/Monaco Telecom technology sharing.",
            "consumer_impact": "Fastest mobile network in Cyprus. Competitive mobile pricing. Growing fiber broadband offering. 5G pioneer.",
            "b2b_impact": "Growing enterprise segment. Mobile fleet management. Limited vs Cyta in enterprise fixed connectivity.",
            "cost_impact": "Lean private-sector cost structure. EIB financing supports FTTH capex. NJJ procurement synergies.",
            "org_culture": "Private-sector agility. Monaco Telecom management. Innovation-focused. Digital-first approach.",
        },
        "cyta_cy": {
            "controlled_vs_resale": "Fully owned fixed + mobile network. National fixed-line incumbent with copper + fiber. FTTP 77% coverage. ~98% own-network.",
            "evolution_strategy": "FTTP expansion toward universal coverage. 5G deployment. Legacy copper retirement. Enterprise ICT growth.",
            "consumer_impact": "Dominant convergent operator. Cytamobile-Vodafone mobile brand. Best fixed coverage. National trust.",
            "b2b_impact": "Cyprus's leading enterprise connectivity provider. Government contracts. Growing managed services.",
            "cost_impact": "High cost base (EUR 148M personnel, ~1,300 employees). State-owned efficiency challenges. Largest revenue base offsets costs.",
            "org_culture": "Semi-governmental institution. Conservative, reliability-focused. Unionized workforce. Modernizing under pressure.",
        },
        "primetel_cy": {
            "controlled_vs_resale": "Own fixed broadband network (partial). Own mobile network (smallest MNO). ~70% own-network.",
            "evolution_strategy": "Broadband and TV growth. Mobile network improvement. Bundle-led competition.",
            "consumer_impact": "Value alternative to Cyta. Competitive broadband pricing. Growing mobile base.",
            "b2b_impact": "Limited enterprise presence. SME-focused connectivity.",
            "cost_impact": "Lean cost structure. Private ownership. Limited capex capacity.",
            "org_culture": "Entrepreneurial alternative operator. Challenger mindset. Agile but resource-constrained.",
        },
    },

    competitive_landscape_notes=[
        "3-player mobile market: Cyta (#1 ~52%), Epic (#2 ~35%), PrimeTel (#3 ~13%)",
        "Cyta is state-owned fixed-line incumbent with Vodafone mobile brand partnership",
        "Epic owned by Monaco Telecom (NJJ/Xavier Niel) — applying private-sector challenger playbook",
        "Cyprus has ~1.43M mobile SIMs for 1.2M population (~120% penetration)",
        "5G launched by Epic (July 2021) and Cyta; coverage expanding",
        "FTTP coverage reaching 77% of premises nationally (Cyta leading)",
        "Small market limits competition intensity; tourism creates seasonal demand",
        "No significant MVNO presence",
    ],

    pest_context={
        "political": [
            "OCECPR regulation; EU Digital Single Market rules apply",
            "Cyta is 100% state-owned — government telecom policy influence",
            "EU member state; full EU regulatory framework",
            "Cyprus division: Republic controls south; northern Cyprus separate telecoms",
            "5G spectrum allocated; deployment underway",
        ],
        "economic": [
            "GDP ~EUR 30B (2024); GDP per capita ~EUR 25,000",
            "GDP growth ~3% (2024); services-driven economy",
            "Inflation ~2.5% (2024)",
            "Tourism major GDP driver (~15% of economy); 4M+ visitors/year",
            "Growing financial services and shipping sectors",
        ],
        "social": [
            "Population ~1.2M (Republic of Cyprus)",
            "Smartphone penetration ~85-90%",
            "Young, educated population; high digital literacy",
            "Large expatriate and tourist communities drive connectivity demand",
            "Seasonal population fluctuations due to tourism",
        ],
        "technological": [
            "5G deployed by Epic and Cyta; coverage expanding",
            "FTTP coverage 77% of premises (Cyta leading rollout)",
            "Strong mobile broadband adoption",
            "Data center growth driven by Cyprus as regional connectivity hub",
            "Smart tourism and e-government initiatives",
        ],
    },
)
