"""Italy telecom market configuration."""

from src.models.market_config import MarketConfig

ITALY_CONFIG = MarketConfig(
    market_id="italy",
    market_name="Italy",
    country="Italy",
    currency="EUR",
    currency_symbol="\u20ac",
    regulatory_body="AGCOM (Autorit\u00e0 per le Garanzie nelle Comunicazioni)",
    population_k=58850,

    customer_segments=[
        {
            "segment_name": "Consumer Premium Convergent",
            "segment_type": "consumer",
            "unmet_needs": [
                "Reliable fiber broadband across all regions (North/South gap)",
                "Seamless fixed-mobile convergent bundles",
            ],
            "pain_points": [
                "Inconsistent fiber availability outside major cities",
                "Complex market structure (network ownership changes)",
            ],
            "purchase_decision_factors": [
                "Network reliability and speed",
                "Bundle value (fixed + mobile)",
                "Brand trust",
                "Local availability of fiber",
            ],
        },
        {
            "segment_name": "Consumer Value-Seeking",
            "segment_type": "consumer",
            "unmet_needs": [
                "Affordable unlimited mobile data plans",
                "Simple, transparent pricing",
            ],
            "pain_points": [
                "Price wars have commoditized mobile; quality differentiation unclear",
                "Frequent operator brand changes confuse customers",
            ],
            "purchase_decision_factors": [
                "Monthly cost",
                "Data allowance (unlimited preferred)",
                "Network coverage (especially South)",
                "Contract flexibility",
            ],
        },
        {
            "segment_name": "Consumer Digital-First / Young",
            "segment_type": "consumer",
            "unmet_needs": [
                "Ultra-competitive SIM-only plans with large data",
                "eSIM and digital-first onboarding",
            ],
            "pain_points": [
                "Many operators still require in-store processes",
                "Limited eSIM adoption vs Northern Europe",
            ],
            "purchase_decision_factors": [
                "Price per GB",
                "Digital experience (app, eSIM)",
                "No contract lock-in",
                "5G access",
            ],
        },
        {
            "segment_name": "Enterprise & Public Sector",
            "segment_type": "enterprise",
            "unmet_needs": [
                "Digitalization of Italian SMEs (vast majority of businesses)",
                "Cloud migration and cybersecurity services",
                "Private 5G for manufacturing (Industry 4.0)",
            ],
            "pain_points": [
                "Fragmented IT landscape among Italian SMEs",
                "North-South digital divide in infrastructure",
            ],
            "purchase_decision_factors": [
                "Reliability and coverage",
                "Managed services capability",
                "Local presence and support",
                "Price competitiveness",
            ],
        },
    ],

    operator_bmc_enrichments={
        "iliad_it": {
            "key_resources": [
                "Growing owned 5G/4G mobile network (6,800+ sites)",
                "Iliad Group technology platform and procurement scale",
                "Strong value-disruptor brand positioning (since 2018 launch)",
                "Digital-first distribution model (online + vending machines)",
            ],
            "value_propositions": [
                "Transparent, aggressive pricing: EUR 9.99/month for 250GB 5G",
                "No hidden fees, no price hikes, forever pricing guarantee",
                "Growing fixed broadband via wholesale fiber (Open Fiber + FiberCop)",
                "Digital-first customer experience (app + eSIM)",
            ],
            "key_partners": [
                "Nokia (RAN vendor for own network)",
                "WindTre (national roaming agreement)",
                "Open Fiber and FiberCop (wholesale fiber access for fixed broadband)",
            ],
            "key_activities": [
                "Own-network buildout (targeting 99% 4G coverage)",
                "5G rollout on 3.5 GHz + 700 MHz spectrum",
                "Fixed broadband rollout via wholesale fiber partnerships",
                "Revenue and subscriber growth in price-competitive market",
            ],
        },
        "tim_it": {
            "key_resources": [
                "Largest customer base in Italy (mobile + fixed)",
                "TIM Enterprise (cloud, IoT, cybersecurity)",
                "Sparkle (international wholesale subsidiary)",
                "Post-NetCo: asset-light model focused on services",
            ],
            "value_propositions": [
                "Premium brand with widest fixed and mobile coverage",
                "Leading enterprise ICT solutions provider in Italy",
                "Converged fixed-mobile bundles (TIM Unica)",
                "Media and entertainment partnerships",
            ],
            "key_partners": [
                "FiberCop/KKR (wholesale fiber access post-NetCo sale)",
                "Google Cloud (enterprise partnership)",
                "DAZN (Serie A football content)",
            ],
            "key_activities": [
                "Post-NetCo transformation to services company",
                "Enterprise and cloud services growth",
                "Customer retention in competitive mobile market",
                "Debt reduction and financial restructuring",
            ],
        },
        "vodafone_it": {
            "key_resources": [
                "Comprehensive mobile network (being integrated with Fastweb)",
                "Fastweb fiber infrastructure (post-merger)",
                "Swisscom ownership bringing Swiss quality and investment",
                "Combined mobile + fixed customer base",
            ],
            "value_propositions": [
                "Post-merger: truly converged fixed-mobile offering",
                "Fastweb fiber speed and quality + Vodafone mobile coverage",
                "Enterprise solutions leveraging combined infrastructure",
                "Brand trust from Vodafone + Fastweb heritage",
            ],
            "key_partners": [
                "Swisscom (new parent company since 2025)",
                "Ericsson (RAN vendor)",
                "Open Fiber (fiber wholesale partnership)",
            ],
            "key_activities": [
                "Fastweb integration and synergy extraction",
                "Network convergence (mobile + fiber)",
                "Customer migration to combined offerings",
                "B2B growth leveraging converged infrastructure",
            ],
        },
        "windtre_it": {
            "key_resources": [
                "Large combined mobile network (ex-Wind + ex-Tre)",
                "CK Hutchison ownership and technology",
                "VERY Mobile sub-brand for value segment",
                "Extensive retail distribution network",
            ],
            "value_propositions": [
                "Comprehensive mobile plans with competitive pricing",
                "VERY Mobile: ultra-low-cost digital brand",
                "Growing fixed broadband via wholesale",
                "Young and digital-savvy brand positioning",
            ],
            "key_partners": [
                "CK Hutchison (parent company)",
                "ZTE and Ericsson (RAN vendors)",
                "Open Fiber (fiber access)",
            ],
            "key_activities": [
                "Network consolidation (Wind + Tre integration complete)",
                "5G rollout and coverage expansion",
                "Fixed broadband growth via wholesale fiber",
                "Cost optimization and efficiency",
            ],
        },
    },

    operator_exposures={
        "iliad_it": [
            {
                "trigger_action": "Still building own network; relies on WindTre roaming for coverage",
                "side_effect": "Network quality perception gap vs established operators",
                "attack_vector": "TIM and Vodafone market superior network quality",
                "severity": "medium",
                "evidence": ["Own network covers ~99% population but indoor coverage gaps remain"],
            },
            {
                "trigger_action": "Fixed broadband heavily dependent on wholesale fiber access",
                "side_effect": "Limited control over fixed broadband quality and pricing",
                "attack_vector": "TIM and Vodafone-Fastweb have own/controlled fixed infrastructure",
                "severity": "high",
                "evidence": ["Iliad fixed broadband uses Open Fiber + FiberCop wholesale"],
            },
            {
                "trigger_action": "Low ARPU model in market with already depressed pricing",
                "side_effect": "Revenue per user among lowest in Europe",
                "attack_vector": "Competitors can invest more per customer in network and services",
                "severity": "medium",
                "evidence": ["Italian mobile ARPU among lowest in Western Europe; Iliad even lower"],
            },
        ],
        "tim_it": [
            {
                "trigger_action": "NetCo sale to KKR transforms TIM into asset-light services company",
                "side_effect": "Lost control of fixed network; now a wholesale customer",
                "attack_vector": "FiberCop could offer same wholesale terms to competitors",
                "severity": "high",
                "evidence": ["NetCo sale completed July 2024; EUR 18.8B transaction"],
            },
            {
                "trigger_action": "Massive debt burden despite NetCo sale proceeds",
                "side_effect": "Limited investment capacity vs well-funded competitors",
                "attack_vector": "Iliad and Vodafone-Fastweb investing aggressively",
                "severity": "medium",
                "evidence": ["TIM net debt reduced but still significant post-sale"],
            },
        ],
        "vodafone_it": [
            {
                "trigger_action": "Fastweb integration complexity and execution risk",
                "side_effect": "Customer disruption during merger integration",
                "attack_vector": "Iliad and TIM target switching customers during transition",
                "severity": "medium",
                "evidence": ["Swisscom completed Vodafone Italia acquisition Jan 2025; integration ongoing"],
            },
            {
                "trigger_action": "Combined entity must rationalize duplicate networks and systems",
                "side_effect": "Integration costs and potential service disruptions",
                "attack_vector": "Competitors capitalize on operational distraction",
                "severity": "medium",
                "evidence": ["Fastweb + Vodafone Italia network integration expected to take 2-3 years"],
            },
        ],
        "windtre_it": [
            {
                "trigger_action": "CK Hutchison evaluating European telecom asset sales",
                "side_effect": "Ownership uncertainty may limit strategic investment",
                "attack_vector": "Competitors invest while WindTre faces ownership limbo",
                "severity": "high",
                "evidence": ["CK Hutchison exploring sale of European telecom assets; discussions with various parties"],
            },
            {
                "trigger_action": "No owned fixed broadband infrastructure",
                "side_effect": "Cannot offer competitive converged bundles without wholesale dependency",
                "attack_vector": "TIM and Vodafone-Fastweb leverage convergence advantage",
                "severity": "medium",
                "evidence": ["WindTre uses wholesale fiber from Open Fiber/FiberCop"],
            },
        ],
    },

    operator_network_enrichments={
        "iliad_it": {
            "controlled_vs_resale": "Own mobile network (6,800+ sites, 99% pop coverage). National roaming on WindTre for gap-fill. Fixed broadband 100% wholesale via Open Fiber + FiberCop. ~70% mobile own-network traffic.",
            "evolution_strategy": "Continue own-network densification. 5G on 3.5 GHz (sub-6) + 700 MHz. Fixed broadband growth via FTTH wholesale. Potential own fiber in dense urban areas long-term.",
            "consumer_impact": "Disruptive pricing (EUR 9.99 for 250GB 5G). Simple transparent tariffs. Growing fixed broadband offering. Digital-first experience.",
            "b2b_impact": "Limited B2B presence. Iliad Business launched for SMEs. Growing but marginal vs TIM Enterprise and Vodafone Business.",
            "cost_impact": "Lean cost structure: highly automated, limited retail. Network build capex elevated but per-sub cost declining as base grows. Iliad Group procurement synergies.",
            "org_culture": "Disruptive challenger DNA from Iliad Group. Engineering-first. Lean and agile. Innovation-focused. Startup culture at growing scale.",
        },
        "tim_it": {
            "controlled_vs_resale": "Fully owned mobile network. Fixed network sold to KKR (FiberCop); now wholesale customer. ~100% mobile own-network, 0% fixed own-network post-NetCo sale.",
            "evolution_strategy": "Asset-light model focused on services and customer relationships. Wholesale fiber from FiberCop. 5G expansion. TIM Enterprise cloud/IoT growth. Sparkle international.",
            "consumer_impact": "Premium brand perception. Widest mobile coverage. Converged bundles via FiberCop wholesale fiber. Serie A football via DAZN partnership.",
            "b2b_impact": "Italy's leading enterprise ICT provider. TIM Enterprise: cloud (Google partnership), cybersecurity, IoT, managed services. Government and public sector contracts.",
            "cost_impact": "Post-NetCo: significantly lower capex but wholesale costs replace network ownership. Workforce reduction ongoing. Debt service remains significant.",
            "org_culture": "Incumbent in transformation. Engineering heritage. Complex stakeholder management (Vivendi, CDP, KKR). New CEO Pietro Labriola driving turnaround.",
        },
        "vodafone_it": {
            "controlled_vs_resale": "Fully owned mobile network (Vodafone) + Fastweb fiber infrastructure (2.5M+ FTTH homepass). Post-merger: ~85% own-network overall. Combined entity controls both mobile and fixed.",
            "evolution_strategy": "Fastweb integration creating convergent operator. Fiber expansion leveraging Fastweb build + Open Fiber access. 5G rollout. Network synergies and rationalization.",
            "consumer_impact": "Post-merger: competitive convergent bundles. Fastweb fiber speed reputation. Vodafone mobile brand trust. Combined offering stronger than either alone.",
            "b2b_impact": "Vodafone Business + Fastweb Enterprise combined. Cloud and connectivity. Growing managed services. Swisscom bringing additional enterprise capabilities.",
            "cost_impact": "Merger synergies EUR 600M+ target over 3-4 years. Network rationalization savings. Swisscom investment commitment. Short-term integration costs.",
            "org_culture": "Integration phase: Vodafone commercial culture meets Fastweb tech culture. Swisscom quality focus. Ambition to become Italy's leading converged operator.",
        },
        "windtre_it": {
            "controlled_vs_resale": "Fully owned mobile network (Wind+Tre merged). No owned fixed infrastructure; wholesale fiber access. ~100% mobile own-network, 0% fixed own-network.",
            "evolution_strategy": "Mobile network optimization and 5G rollout. Fixed broadband via wholesale. VERY Mobile sub-brand for value. Exploring strategic options under CK Hutchison.",
            "consumer_impact": "Competitive mobile plans. VERY Mobile for ultra-value. Growing fixed broadband via wholesale. Young brand positioning.",
            "b2b_impact": "WindTre Business for SME segment. Limited large enterprise capability. B2B a smaller focus than consumer.",
            "cost_impact": "Wind+Tre merger synergies mostly realized. Lean operating model. CK Hutchison cost discipline. No fixed network capex.",
            "org_culture": "Post-merger stabilized. CK Hutchison management style. Cost-conscious. Focused on mobile profitability.",
        },
    },

    competitive_landscape_notes=[
        "4-player mobile market: TIM (incumbent), Vodafone-Fastweb (converging), WindTre, Iliad (disruptor)",
        "Among most price-competitive markets in Europe; Iliad's 2018 entry further depressed ARPUs",
        "TIM NetCo sale to KKR (2024) fundamentally restructured fixed-line competition",
        "Vodafone Italia + Fastweb merger under Swisscom creating strong convergent #2",
        "CK Hutchison potentially selling WindTre, further restructuring possible",
        "Fiber rollout via Open Fiber (wholesale) and FiberCop (ex-TIM network) creates infrastructure competition",
        "5G deployed by all operators; coverage expanding with 3.5 GHz",
        "AGCOM promoting competition; spectrum and wholesale access regulation",
    ],

    pest_context={
        "political": [
            "AGCOM regulation promoting infrastructure competition and wholesale access",
            "Italian government involvement in TIM restructuring (CDP stake)",
            "EU Digital Decade targets driving broadband investment",
            "5G spectrum auction completed 2018 (raised EUR 6.5B — very high)",
            "Italian Recovery and Resilience Plan (PNRR) funding broadband expansion",
        ],
        "economic": [
            "GDP per capita ~EUR 34,000; significant North-South gap",
            "GDP growth ~0.5-1.0%; below EU average",
            "Inflation normalizing to ~2% after 2022-23 spike",
            "High public debt constraining government investment capacity",
        ],
        "social": [
            "Population ~58.9M; aging and declining demographics",
            "Smartphone penetration ~85%",
            "Strong mobile-first culture; fixed broadband penetration lower than NW Europe",
            "Digital skills gap; government digital inclusion initiatives",
            "Growing remote work adoption driving fiber demand",
        ],
        "technological": [
            "5G rollout by all operators; Italy was early EU adopter (2018 auction)",
            "Fiber FTTH rollout via Open Fiber + FiberCop; targeting 85% coverage by 2026",
            "VHCN coverage ~65% of premises; EU Digital Decade target 100% by 2030",
            "Smart city and IoT initiatives in Milan, Rome, Turin",
            "TIM NetCo/FiberCop under KKR — single wholesale fiber platform",
        ],
    },
)
