"""Extract structured data from the 8 deep analysis MD files.

Reads each MD, parses tables/metrics, and outputs a DeepAnalysisData
dataclass suitable for PPT generation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from src.output.md_parser import (
    parse_md_table,
    parse_md_tables_all,
    extract_section,
    extract_bullet_items,
    extract_number,
    extract_metric_value,
    parse_number,
    extract_code_block,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class MarketSnapshot:
    market_size: str = "€12.3B"
    market_growth: str = "+0.3%"
    hhi: str = "~3,500+"
    lifecycle: str = "Mature"
    revenue_distribution: list[dict] = field(default_factory=list)
    # Operator shares
    dt_share: str = "50.3%"
    vf_share: str = "25.1%"
    o2_share: str = "16.2%"
    oneandone_share: str = "8.4%"


@dataclass
class VodafonePosition:
    revenue: str = "€3,092M"
    revenue_rank: str = "#2"
    ebitda_margin: str = "36.2%"
    mobile_subs: str = "32,500K"
    bb_subs: str = "9,940K"
    tv_subs: str = "7,740K"
    churn: str = "1.05%"
    fiveg_coverage: str = "92%"
    mobile_net_adds: str = "+80K/q"
    bb_net_adds: str = "-63K/q"
    b2b_revenue: str = "€520M/q"
    wholesale_revenue: str = "€380M/q"
    fmc_subs: str = "4,900K"
    fmc_penetration: str = "49.3%"


@dataclass
class PESTData:
    overall_assessment: str = ""
    political_factors: list[dict] = field(default_factory=list)
    economic_factors: list[dict] = field(default_factory=list)
    social_factors: list[dict] = field(default_factory=list)
    technology_factors: list[dict] = field(default_factory=list)
    pest_weather: list[dict] = field(default_factory=list)
    factor_ranking: list[dict] = field(default_factory=list)
    ksf_table: list[dict] = field(default_factory=list)
    value_transfers: list[dict] = field(default_factory=list)


@dataclass
class APPEALSData:
    dimensions: list[dict] = field(default_factory=list)  # rows from 4.1 table
    gaps: list[dict] = field(default_factory=list)
    diagnosis_items: list[str] = field(default_factory=list)


@dataclass
class MarketCustomerData:
    snapshot_table: list[dict] = field(default_factory=list)
    share_table: list[dict] = field(default_factory=list)
    segments: list[dict] = field(default_factory=list)
    appeals: APPEALSData = field(default_factory=APPEALSData)
    events: list[dict] = field(default_factory=list)
    value_migration: list[dict] = field(default_factory=list)
    opportunities: list[dict] = field(default_factory=list)
    threats: list[dict] = field(default_factory=list)


@dataclass
class TariffData:
    mobile_postpaid_table: list[dict] = field(default_factory=list)
    price_gap_table: list[dict] = field(default_factory=list)
    eur_per_gb: list[dict] = field(default_factory=list)
    vf_evolution: list[dict] = field(default_factory=list)
    dt_evolution: list[dict] = field(default_factory=list)
    o2_evolution: list[dict] = field(default_factory=list)
    oneandone_evolution: list[dict] = field(default_factory=list)
    dsl_table: list[dict] = field(default_factory=list)
    cable_table: list[dict] = field(default_factory=list)
    fiber_table: list[dict] = field(default_factory=list)
    fmc_table: list[dict] = field(default_factory=list)
    fiveg_erosion: list[dict] = field(default_factory=list)
    strategic_insights: list[str] = field(default_factory=list)


@dataclass
class CompetitorProfile:
    name: str = ""
    financial_table: list[dict] = field(default_factory=list)
    subscriber_table: list[dict] = field(default_factory=list)
    strategy_summary: str = ""
    strategy_items: list[str] = field(default_factory=list)
    threat_to_vf: str = ""
    opportunity_for_vf: str = ""


@dataclass
class CompetitionData:
    market_structure: list[dict] = field(default_factory=list)
    growth_trajectories: list[dict] = field(default_factory=list)
    five_forces: list[dict] = field(default_factory=list)
    competitors: list[CompetitorProfile] = field(default_factory=list)
    financial_benchmark: list[dict] = field(default_factory=list)
    subscriber_benchmark: list[dict] = field(default_factory=list)
    network_benchmark: list[dict] = field(default_factory=list)
    competitive_radar: list[dict] = field(default_factory=list)
    squeezed_middle: list[dict] = field(default_factory=list)
    priorities: list[dict] = field(default_factory=list)
    response_matrix: list[dict] = field(default_factory=list)


@dataclass
class SelfAnalysisData:
    top_kpis: list[dict] = field(default_factory=list)
    revenue_trend: list[dict] = field(default_factory=list)
    capex_efficiency: list[dict] = field(default_factory=list)
    revenue_mix: list[dict] = field(default_factory=list)
    wholesale_trend: list[dict] = field(default_factory=list)
    mobile_segment: list[dict] = field(default_factory=list)
    fixed_segment: list[dict] = field(default_factory=list)
    b2b_segment: list[dict] = field(default_factory=list)
    tv_segment: list[dict] = field(default_factory=list)
    position_table: list[dict] = field(default_factory=list)
    network_infra: list[dict] = field(default_factory=list)
    tech_stack: list[dict] = field(default_factory=list)
    bmc_table: list[dict] = field(default_factory=list)
    bmc_vulnerability: list[dict] = field(default_factory=list)
    strengths: list[dict] = field(default_factory=list)
    weaknesses: list[dict] = field(default_factory=list)
    exposure_points: list[dict] = field(default_factory=list)
    health_scorecard: list[dict] = field(default_factory=list)
    must_change: list[dict] = field(default_factory=list)
    working_well: list[dict] = field(default_factory=list)
    management_statements: list[dict] = field(default_factory=list)


@dataclass
class SWOTData:
    posture: str = ""
    overview_table: list[dict] = field(default_factory=list)
    strengths: list[dict] = field(default_factory=list)
    weaknesses: list[dict] = field(default_factory=list)
    opportunities: list[dict] = field(default_factory=list)
    threats: list[dict] = field(default_factory=list)
    strengths_vs_dt: list[dict] = field(default_factory=list)
    so_strategies: list[dict] = field(default_factory=list)
    wo_strategies: list[dict] = field(default_factory=list)
    st_strategies: list[dict] = field(default_factory=list)
    wt_strategies: list[dict] = field(default_factory=list)
    squeezed_middle: list[dict] = field(default_factory=list)
    strategic_priorities: list[dict] = field(default_factory=list)
    what_not_to_do: list[str] = field(default_factory=list)


@dataclass
class OpportunityItem:
    name: str = ""
    span_ma: float = 0.0
    span_cp: float = 0.0
    quadrant: str = "grow_invest"
    priority: str = "P1"
    revenue_impact: str = ""
    timeline: str = ""
    investment: str = ""
    description: str = ""


@dataclass
class OpportunitiesData:
    quadrant_summary: list[dict] = field(default_factory=list)
    opportunities: list[OpportunityItem] = field(default_factory=list)
    acquire_skills: list[dict] = field(default_factory=list)
    priority_matrix: list[dict] = field(default_factory=list)
    financial_impact: list[dict] = field(default_factory=list)
    investment_table: list[dict] = field(default_factory=list)
    net_value: list[dict] = field(default_factory=list)
    success_metrics: list[dict] = field(default_factory=list)
    immediate_actions: list[str] = field(default_factory=list)


@dataclass
class ExecutiveSummaryData:
    verdict: str = ""
    market: MarketSnapshot = field(default_factory=MarketSnapshot)
    position: VodafonePosition = field(default_factory=VodafonePosition)
    look_findings: list[dict] = field(default_factory=list)
    squeezed_middle_table: list[dict] = field(default_factory=list)
    priorities: list[dict] = field(default_factory=list)
    what_not_to_do: list[dict] = field(default_factory=list)
    risk_bull: list[dict] = field(default_factory=list)
    risk_bear: list[dict] = field(default_factory=list)
    risk_net: list[dict] = field(default_factory=list)
    kpi_dashboard: list[dict] = field(default_factory=list)
    timeline_text: str = ""


@dataclass
class DeepAnalysisData:
    executive: ExecutiveSummaryData = field(default_factory=ExecutiveSummaryData)
    trends: PESTData = field(default_factory=PESTData)
    market_customer: MarketCustomerData = field(default_factory=MarketCustomerData)
    tariff: TariffData = field(default_factory=TariffData)
    competition: CompetitionData = field(default_factory=CompetitionData)
    self_analysis: SelfAnalysisData = field(default_factory=SelfAnalysisData)
    swot: SWOTData = field(default_factory=SWOTData)
    opportunities: OpportunitiesData = field(default_factory=OpportunitiesData)


# ---------------------------------------------------------------------------
# Extraction logic
# ---------------------------------------------------------------------------

def _find_table_after(text: str, heading_fragment: str) -> list[dict]:
    """Find the first table after a heading containing the fragment."""
    idx = text.lower().find(heading_fragment.lower())
    if idx < 0:
        return []
    remainder = text[idx:]
    tables = parse_md_tables_all(remainder)
    return tables[0] if tables else []


def _extract_text_between(text: str, start_pattern: str, end_pattern: str) -> str:
    """Extract text between two patterns."""
    start = re.search(start_pattern, text, re.IGNORECASE)
    if not start:
        return ""
    after = text[start.end():]
    end = re.search(end_pattern, after, re.IGNORECASE)
    if end:
        return after[:end.start()].strip()
    return after[:500].strip()


def extract_executive_summary(text: str) -> ExecutiveSummaryData:
    data = ExecutiveSummaryData()

    # Verdict
    match = re.search(r'\*\*(.+?trapped.+?)\*\*', text)
    if match:
        data.verdict = match.group(1)

    # All tables
    tables = parse_md_tables_all(text)

    # Section 1.1 Market Context
    data.executive = data  # self-ref not needed, but keep field assignments

    # Find specific tables by nearby headings
    data.look_findings = []
    for look_name in ['Look 1', 'Look 2', 'Look 3', 'Look 4', 'Tariff', 'SWOT', 'Look 5']:
        table = _find_table_after(text, look_name)
        if table:
            data.look_findings.append({'section': look_name, 'rows': table})

    # Squeezed middle table (Section 3)
    data.squeezed_middle_table = _find_table_after(text, 'Squeezed Middle')

    # Priorities (Section 4)
    for p in ['Priority 1', 'Priority 2', 'Priority 3', 'Priority 4', 'Priority 5']:
        t = _find_table_after(text, p)
        if t:
            data.priorities.append({'name': p, 'rows': t})

    # What NOT to do
    data.what_not_to_do = _find_table_after(text, 'What NOT to Do')

    # Risk tables
    data.risk_bull = _find_table_after(text, 'Bull Case')
    data.risk_bear = _find_table_after(text, "Doesn't Execute")
    data.risk_net = _find_table_after(text, 'Net Assessment')

    # KPI dashboard
    data.kpi_dashboard = _find_table_after(text, 'Success Metrics')

    # Timeline
    data.timeline_text = extract_code_block(text)

    return data


def extract_trends(text: str) -> PESTData:
    data = PESTData()

    # PEST weather table
    data.pest_weather = _find_table_after(text, 'Overall PEST Weather')

    # Factor ranking
    data.factor_ranking = _find_table_after(text, 'Factor Priority Ranking')

    # Political factors
    political_section = extract_section(text, 'Political Factors', level=2)
    if political_section:
        tables = parse_md_tables_all(political_section)
        data.political_factors = tables

    # Economic
    econ_section = extract_section(text, 'Economic Factors', level=2)
    if econ_section:
        data.economic_factors = parse_md_tables_all(econ_section)

    # Social
    social_section = extract_section(text, 'Social Factors', level=2)
    if social_section:
        data.social_factors = parse_md_tables_all(social_section)

    # Technology
    tech_section = extract_section(text, 'Technology Factors', level=2)
    if tech_section:
        data.technology_factors = parse_md_tables_all(tech_section)

    # KSF
    data.ksf_table = _find_table_after(text, 'Key Success Factors')

    # Value transfers
    data.value_transfers = _find_table_after(text, 'Value Migration Map')

    # Net assessment
    match = re.search(r'Overall:\s*(.+)', text)
    if match:
        data.overall_assessment = match.group(1).strip()

    return data


def extract_market_customer(text: str) -> MarketCustomerData:
    data = MarketCustomerData()

    data.snapshot_table = _find_table_after(text, 'Market Fundamentals')
    data.share_table = _find_table_after(text, 'Market Share Structure')

    # Segments
    seg_section = extract_section(text, 'Customer Segmentation', level=2)
    if not seg_section:
        seg_section = extract_section(text, 'Segment Portfolio', level=3)
    data.segments = _find_table_after(text, 'Segment Portfolio')

    # Events
    data.events = _find_table_after(text, 'Top 10 Market Events')

    # APPEALS
    appeals_table = _find_table_after(text, 'Dimension Scores')
    data.appeals = APPEALSData(
        dimensions=appeals_table,
        gaps=_find_table_after(text, 'Critical Gaps'),
    )

    # Value migration
    data.value_migration = _find_table_after(text, 'Migration Patterns')

    # Opportunities & Threats
    data.opportunities = _find_table_after(text, 'Opportunities (Ranked)')
    data.threats = _find_table_after(text, 'Threats (Ranked)')

    return data


def extract_tariff(text: str) -> TariffData:
    data = TariffData()

    data.price_gap_table = _find_table_after(text, 'Same-Tier Price Gap')
    data.mobile_postpaid_table = _find_table_after(text, 'Full Price Table')
    data.eur_per_gb = _find_table_after(text, 'Value Analysis')

    # Evolution tables per operator
    data.vf_evolution = _find_table_after(text, 'Vodafone Germany')
    data.dt_evolution = _find_table_after(text, 'Deutsche Telekom')
    data.o2_evolution = _find_table_after(text, 'Most Aggressive')
    data.oneandone_evolution = _find_table_after(text, 'MVNO-to-MNO')

    # Fixed
    data.dsl_table = _find_table_after(text, 'DSL')
    data.cable_table = _find_table_after(text, 'Cable')
    data.fiber_table = _find_table_after(text, 'Fiber (FTTH)')
    data.fmc_table = _find_table_after(text, 'FMC Bundle')

    # 5G erosion
    data.fiveg_erosion = _find_table_after(text, '5G Premium Erosion')

    # Strategic insights
    insight_section = extract_section(text, 'Strategic Implications', level=2)
    if insight_section:
        data.strategic_insights = extract_bullet_items(insight_section)
        # Also get subsection key insights
        for sub in ['Squeezed Middle', 'Crown Jewel', 'Low-End', 'Competitive Equalizer']:
            s = extract_section(insight_section, sub, level=3)
            if s:
                items = extract_bullet_items(s)
                data.strategic_insights.extend(items)

    return data


def extract_competition(text: str) -> CompetitionData:
    data = CompetitionData()

    data.market_structure = _find_table_after(text, 'Four-Player Oligopoly')
    data.growth_trajectories = _find_table_after(text, 'Growth Trajectories')
    data.five_forces = _find_table_after(text, 'Force Summary')

    # Competitor profiles
    for name, heading in [
        ('Deutsche Telekom', 'Deutsche Telekom'),
        ('Telefonica O2', 'O2'),
        ('1&1 AG', '1&1 AG'),
    ]:
        profile = CompetitorProfile(name=name)
        section = extract_section(text, heading, level=3)
        if section:
            tables = parse_md_tables_all(section)
            if len(tables) >= 1:
                profile.financial_table = tables[0]
            if len(tables) >= 2:
                profile.subscriber_table = tables[1]
            # Strategy summary
            strat_match = re.search(r'\*\*"(.+?)"\*\*', section)
            if strat_match:
                profile.strategy_summary = strat_match.group(1)
            # Numbered strategy items
            numbered = re.findall(r'^\d+\.\s+\*\*(.+?)\*\*', section, re.MULTILINE)
            profile.strategy_items = numbered[:5]
            # Threat/opportunity
            threat_match = re.search(r'\*\*Threat to Vodafone\*\*:\s*(.+?)(?:\n\n|\Z)', section, re.DOTALL)
            if threat_match:
                profile.threat_to_vf = threat_match.group(1).strip()[:200]
            opp_match = re.search(r'\*\*Opportunity for Vodafone\*\*:\s*(.+?)(?:\n\n|\Z)', section, re.DOTALL)
            if opp_match:
                profile.opportunity_for_vf = opp_match.group(1).strip()[:200]
        data.competitors.append(profile)

    # Benchmarks
    data.financial_benchmark = _find_table_after(text, 'Financial Benchmarking')
    data.subscriber_benchmark = _find_table_after(text, 'Subscriber Benchmarking')
    data.network_benchmark = _find_table_after(text, 'Network Benchmarking')
    data.competitive_radar = _find_table_after(text, 'Competitive Strength Radar')
    data.squeezed_middle = _find_table_after(text, 'Squeezed Middle')
    data.priorities = _find_table_after(text, 'Five Competitive Priorities')
    data.response_matrix = _find_table_after(text, 'Competitive Response Matrix')

    return data


def extract_self_analysis(text: str) -> SelfAnalysisData:
    data = SelfAnalysisData()

    data.top_kpis = _find_table_after(text, 'Top-Line KPIs')
    data.revenue_trend = _find_table_after(text, 'Revenue Trend')
    data.capex_efficiency = _find_table_after(text, 'Capex Efficiency')
    data.revenue_mix = _find_table_after(text, 'Revenue Mix')
    data.wholesale_trend = _find_table_after(text, '1&1 Effect')

    # Segments
    data.mobile_segment = _find_table_after(text, 'Mobile')
    data.fixed_segment = _find_table_after(text, 'Fixed Broadband')
    data.b2b_segment = _find_table_after(text, 'B2B/Enterprise')
    data.tv_segment = _find_table_after(text, 'TV/Convergence')

    # Position
    data.position_table = _find_table_after(text, 'Position by Metric')

    # Network
    data.network_infra = _find_table_after(text, 'Network Infrastructure')
    data.tech_stack = _find_table_after(text, 'Technology Stack')

    # BMC
    data.bmc_table = _find_table_after(text, 'BMC Overview')
    data.bmc_vulnerability = _find_table_after(text, 'BMC Vulnerability')

    # S/W/E
    data.strengths = _find_table_after(text, 'Strengths')
    data.weaknesses = _find_table_after(text, 'Weaknesses')
    data.exposure_points = _find_table_after(text, 'Exposure Points')

    # Diagnosis
    data.health_scorecard = _find_table_after(text, 'Health Scorecard')
    data.must_change = _find_table_after(text, 'Three Things That Must Change')
    data.working_well = _find_table_after(text, 'Three Things Working Well')
    data.management_statements = _find_table_after(text, 'Key Management Statements')

    return data


def extract_swot(text: str) -> SWOTData:
    data = SWOTData()

    data.overview_table = _find_table_after(text, 'Posture Assessment')

    # Posture
    match = re.search(r'Strategic posture:\s*\*\*(.+?)\*\*', text)
    if match:
        data.posture = match.group(1)

    # SWOT items
    data.strengths = _find_table_after(text, 'Strength Portfolio')
    data.weaknesses = _find_table_after(text, 'Weakness Portfolio')
    data.opportunities = _find_table_after(text, 'Opportunity Portfolio')
    data.threats = _find_table_after(text, 'Threat Portfolio')

    # Strengths vs DT
    data.strengths_vs_dt = _find_table_after(text, 'Strengths vs DT')

    # Strategy matrices
    data.so_strategies = _find_table_after(text, 'SO Strategies')
    data.wo_strategies = _find_table_after(text, 'WO Strategies')
    data.st_strategies = _find_table_after(text, 'ST Strategies')
    data.wt_strategies = _find_table_after(text, 'WT Strategies')

    # Squeezed middle
    data.squeezed_middle = _find_table_after(text, 'Squeezed Middle')

    # Priorities
    data.strategic_priorities = _find_table_after(text, 'Five Strategic Priorities')

    # What not to do
    not_to_do_section = extract_section(text, 'What NOT to Do', level=3)
    if not_to_do_section:
        data.what_not_to_do = extract_bullet_items(not_to_do_section)
        if not data.what_not_to_do:
            # Try numbered items
            data.what_not_to_do = re.findall(
                r'\d+\.\s+\*\*(.+?)\*\*', not_to_do_section)

    return data


def extract_opportunities(text: str) -> OpportunitiesData:
    data = OpportunitiesData()

    data.quadrant_summary = _find_table_after(text, 'Quadrant Distribution')

    # Build opportunity items from subsections
    opps = []
    # Tier 1
    for name, heading in [
        ('FibreCo JV', 'FibreCo JV'),
        ('Spectrum Extension', 'Spectrum Extension'),
        ('Gigabit Funding', 'Gigabit Funding'),
        ('1&1 Wholesale', '1&1 Wholesale'),
    ]:
        item = _parse_opportunity_section(text, name, heading, 'P0')
        if item:
            opps.append(item)
    # Tier 2
    for name, heading in [
        ('Skaylink B2B', 'Skaylink'),
        ('FMC Convergence', 'FMC Convergence'),
        ('Cable Restructuring', 'Cable TV Frequency'),
    ]:
        item = _parse_opportunity_section(text, name, heading, 'P0')
        if item:
            opps.append(item)
    # Tier 3
    for name, heading in [
        ('5G Enterprise', '5G Enterprise'),
        ('AI/ML Network', 'AI/ML'),
        ('Open RAN', 'Open RAN'),
    ]:
        item = _parse_opportunity_section(text, name, heading, 'P2')
        if item:
            opps.append(item)
    # SO strategies
    for name, heading in [
        ('SO-1: Brand Regulatory', 'SO-1'),
        ('SO-2: Enterprise Digital', 'SO-2'),
        ('SO-3: Network Spectrum', 'SO-3'),
        ('SO-4: EBITDA Gigabit', 'SO-4'),
    ]:
        item = _parse_opportunity_section(text, name, heading, 'P0')
        if item:
            opps.append(item)
    # WO strategies
    for name, heading in [
        ('WO-1: Customer Service', 'WO-1'),
        ('WO-2: Pricing Narrative', 'WO-2'),
        ('WO-3: Wholesale Transition', 'WO-3'),
    ]:
        item = _parse_opportunity_section(text, name, heading, 'P1')
        if item:
            opps.append(item)

    data.opportunities = opps

    # Acquire skills
    data.acquire_skills = _find_table_after(text, 'Acquire Skills')
    if not data.acquire_skills:
        data.acquire_skills = _find_table_after(text, 'Capability Gaps')

    # Priority matrix
    data.priority_matrix = _find_table_after(text, 'Priority Matrix')

    # Financial impact
    data.financial_impact = _find_table_after(text, 'Revenue Impact')
    data.investment_table = _find_table_after(text, 'Investment Requirements')
    data.net_value = _find_table_after(text, 'Net Value Creation')
    data.success_metrics = _find_table_after(text, 'Success Metrics')

    # Immediate actions
    imm_section = extract_section(text, 'Immediate Actions', level=3)
    if imm_section:
        data.immediate_actions = extract_bullet_items(imm_section)
        if not data.immediate_actions:
            data.immediate_actions = re.findall(
                r'\d+\.\s+\*\*(.+?)\*\*', imm_section)

    return data


def _parse_opportunity_section(
    text: str, name: str, heading: str, default_priority: str
) -> Optional[OpportunityItem]:
    """Parse an opportunity from the MD."""
    idx = text.find(heading)
    if idx < 0:
        return None
    section = text[idx:idx + 1500]

    item = OpportunityItem(name=name, priority=default_priority)

    # SPAN scores
    ma_match = re.search(r'Market Attractiveness:\s*([\d.]+)', section)
    cp_match = re.search(r'Competitive Position:\s*([\d.]+)', section)
    if ma_match:
        item.span_ma = float(ma_match.group(1))
    if cp_match:
        item.span_cp = float(cp_match.group(1))

    # Quadrant
    if item.span_ma >= 5 and item.span_cp >= 5:
        item.quadrant = 'grow_invest'
    elif item.span_ma >= 5:
        item.quadrant = 'acquire_skills'
    else:
        item.quadrant = 'harvest'

    # Priority override
    prio_match = re.search(r'Priority\*?\*?\s*\|\s*\*?\*?(P[012])', section)
    if prio_match:
        item.priority = prio_match.group(1)

    # Revenue
    rev_match = re.search(r'Revenue (?:Impact|potential)[:\s]*\|?\s*([^|\n]+)', section, re.IGNORECASE)
    if rev_match:
        item.revenue_impact = rev_match.group(1).strip().strip('|* ')

    # Timeline
    time_match = re.search(r'(?:Payoff horizon|Timeline)[:\s]*\|?\s*([^|\n]+)', section, re.IGNORECASE)
    if time_match:
        item.timeline = time_match.group(1).strip().strip('|* ')

    # Investment
    inv_match = re.search(r'Investment[:\s]*\|?\s*([^|\n]+)', section, re.IGNORECASE)
    if inv_match:
        item.investment = inv_match.group(1).strip().strip('|* ')

    # Strategic value as description
    sv_match = re.search(r'Strategic value[:\s]*\|?\s*\*?\*?([^|\n]+)', section, re.IGNORECASE)
    if sv_match:
        item.description = sv_match.group(1).strip().strip('|* ')

    return item


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def load_deep_analysis(data_dir: str = "data/output") -> DeepAnalysisData:
    """Load and parse all 8 deep analysis MD files.

    Args:
        data_dir: Path to directory containing the MD files.

    Returns:
        DeepAnalysisData with all parsed content.
    """
    base = Path(data_dir)
    result = DeepAnalysisData()

    # Map files
    file_map = {
        'executive': 'executive_summary_cq4_2025.md',
        'trends': 'trends_deep_analysis_cq4_2025.md',
        'market_customer': 'market_customer_deep_analysis_cq4_2025.md',
        'tariff': 'tariff_deep_analysis_h1_2026.md',
        'competition': 'competition_deep_analysis_cq4_2025.md',
        'self_analysis': 'self_analysis_deep_cq4_2025.md',
        'swot': 'swot_deep_analysis_cq4_2025.md',
        'opportunities': 'opportunities_deep_analysis_cq4_2025.md',
    }

    extractors = {
        'executive': extract_executive_summary,
        'trends': extract_trends,
        'market_customer': extract_market_customer,
        'tariff': extract_tariff,
        'competition': extract_competition,
        'self_analysis': extract_self_analysis,
        'swot': extract_swot,
        'opportunities': extract_opportunities,
    }

    for key, filename in file_map.items():
        filepath = base / filename
        if filepath.exists():
            text = filepath.read_text(encoding='utf-8')
            extractor = extractors[key]
            setattr(result, key, extractor(text))
        else:
            print(f"Warning: {filepath} not found")

    return result
