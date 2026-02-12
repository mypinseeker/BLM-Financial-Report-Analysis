"""BLM Five Looks Analysis Engine - Main Entry Point.

Orchestrates the complete five looks + SWOT analysis pipeline:
  1. Look at Trends (PEST Framework)
  2. Look at Market/Customer ($APPEALS)
  3. Look at Competition (Porter's Five Forces)
  4. Look at Self (BMC + Capability Assessment)
  5. SWOT Synthesis (Bridge)
  6. Look at Opportunities (SPAN Matrix)

Usage:
    from src.database.db import TelecomDatabase
    from src.blm.engine import BLMAnalysisEngine

    db = TelecomDatabase("data/telecom.db")
    engine = BLMAnalysisEngine(db, target_operator="vodafone_germany", market="germany")
    result = engine.run_five_looks()
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.models.market_configs import get_market_config
from src.models.provenance import ProvenanceStore, SourceReference, SourceType, Confidence


@dataclass
class FiveLooksResult:
    """Complete output of the five looks analysis."""

    target_operator: str
    market: str
    analysis_period: str  # calendar quarter, e.g. "CQ4_2025"

    trends: object = None  # TrendAnalysis
    market_customer: object = None  # MarketCustomerInsight
    competition: object = None  # CompetitionInsight
    self_analysis: object = None  # SelfInsight
    swot: object = None  # SWOTAnalysis
    opportunities: object = None  # OpportunityInsight
    tariff_analysis: object = None  # dict from analyze_tariffs()

    provenance: ProvenanceStore = field(default_factory=ProvenanceStore)


class BLMAnalysisEngine:
    """Orchestrates the Five Looks + SWOT analysis pipeline.

    Sequence: Trends -> Market/Customer -> Competition -> Self -> SWOT -> Opportunities
    """

    def __init__(
        self,
        db,
        target_operator: str,
        market: str,
        target_period: Optional[str] = None,
        n_quarters: int = 8,
    ):
        self.db = db
        self.target_operator = target_operator
        self.market = market
        self.target_period = target_period
        self.n_quarters = n_quarters
        self.provenance = ProvenanceStore()
        self.market_config = get_market_config(market)

    def run_five_looks(self) -> FiveLooksResult:
        """Execute the complete five looks analysis pipeline."""
        trends = self.look_at_trends()
        market_customer = self.look_at_market_customer()
        competition = self.look_at_competition()
        tariff_analysis = self._analyze_tariffs()
        self_analysis = self.look_at_self()
        swot = self.synthesize_swot(trends, market_customer, competition, self_analysis)
        opportunities = self.look_at_opportunities(
            trends, market_customer, competition, self_analysis, swot
        )
        self._wire_provenance()

        return FiveLooksResult(
            target_operator=self.target_operator,
            market=self.market,
            analysis_period=self.target_period or self._determine_latest_period(),
            trends=trends,
            market_customer=market_customer,
            competition=competition,
            self_analysis=self_analysis,
            swot=swot,
            opportunities=opportunities,
            tariff_analysis=tariff_analysis,
            provenance=self.provenance,
        )

    def look_at_trends(self):
        """01 Look at Trends - PEST Framework.

        Input tables: macro_environment, intelligence_events
        Output: TrendAnalysis
        """
        from src.blm.look_at_trends import analyze_trends

        return analyze_trends(
            db=self.db,
            market=self.market,
            target_operator=self.target_operator,
            target_period=self.target_period,
            n_quarters=self.n_quarters,
            provenance=self.provenance,
            market_config=self.market_config,
        )

    def look_at_market_customer(self):
        """02 Look at Market/Customer - Market changes + $APPEALS.

        Input tables: financial_quarterly, subscriber_quarterly, tariffs, intelligence_events
        Output: MarketCustomerInsight
        """
        from src.blm.look_at_market_customer import analyze_market_customer

        return analyze_market_customer(
            db=self.db,
            market=self.market,
            target_operator=self.target_operator,
            target_period=self.target_period,
            n_quarters=self.n_quarters,
            provenance=self.provenance,
            market_config=self.market_config,
        )

    def look_at_competition(self):
        """03 Look at Competition - Porter's Five Forces.

        Input tables: all tables for all operators in the market
        Output: CompetitionInsight
        """
        from src.blm.look_at_competition import analyze_competition

        return analyze_competition(
            db=self.db,
            market=self.market,
            target_operator=self.target_operator,
            target_period=self.target_period,
            n_quarters=self.n_quarters,
            market_config=self.market_config,
            provenance=self.provenance,
        )

    def look_at_self(self):
        """04 Look at Self - BMC + Capability Assessment.

        Input tables: target operator's full data + competitor data for comparison
        Output: SelfInsight
        """
        from src.blm.look_at_self import analyze_self

        return analyze_self(
            db=self.db,
            market=self.market,
            target_operator=self.target_operator,
            target_period=self.target_period,
            n_quarters=self.n_quarters,
            provenance=self.provenance,
            market_config=self.market_config,
        )

    def synthesize_swot(self, trends, market_customer, competition, self_analysis):
        """SWOT Synthesis - Bridge between Look 4 and Look 5.

        Extracts:
          S <- self_analysis.strengths
          W <- self_analysis.weaknesses + exposure_points
          O <- trends opportunities + market_customer.opportunities
          T <- trends threats + market_customer.threats + competition pressures
        """
        from src.blm.swot_synthesis import synthesize_swot

        return synthesize_swot(
            trends=trends,
            market_customer=market_customer,
            competition=competition,
            self_analysis=self_analysis,
            provenance=self.provenance,
        )

    def look_at_opportunities(
        self, trends, market_customer, competition, self_analysis, swot
    ):
        """05 Look at Opportunities - SPAN Matrix.

        Cross-derives opportunity items from all previous analyses.
        Scores each on market attractiveness x competitive position.
        """
        from src.blm.look_at_opportunities import analyze_opportunities

        return analyze_opportunities(
            trends=trends,
            market_customer=market_customer,
            competition=competition,
            self_analysis=self_analysis,
            swot=swot,
            db=self.db,
            target_operator=self.target_operator,
            provenance=self.provenance,
        )

    def _analyze_tariffs(self):
        """Run tariff deep-analysis across all operators in the market."""
        try:
            from src.blm.analyze_tariffs import analyze_tariffs

            return analyze_tariffs(
                db=self.db,
                market=self.market,
                target_operator=self.target_operator,
            )
        except Exception:
            return None

    def _wire_provenance(self):
        """Aggregate source_urls from DB tables into the provenance store.

        Scans intelligence_events and earnings_call_highlights for source_urls,
        registers them as SourceReferences, and upgrades tracked values that
        come from sourced data to medium/high confidence.
        """
        seen_urls: set[str] = set()

        # 1. Intelligence events
        try:
            events = self.db.get_intelligence_events(
                market=self.market, days_back=730
            )
            for ev in events:
                url = ev.get("source_url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    src = SourceReference(
                        source_type=SourceType.NEWS_ARTICLE,
                        url=url,
                        document_name=ev.get("title", ""),
                        data_period=ev.get("event_date", ""),
                        confidence=Confidence.MEDIUM,
                    )
                    self.provenance.register_source(src)
        except Exception:
            pass

        # 2. Earnings call highlights
        try:
            latest_cq = self.target_period or self._determine_latest_period()
            highlights = self.db.get_earnings_highlights(
                self.target_operator, latest_cq
            )
            for h in highlights:
                url = h.get("source_url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    src = SourceReference(
                        source_type=SourceType.EARNINGS_CALL_TRANSCRIPT,
                        url=url,
                        document_name=f"{self.target_operator} earnings",
                        publisher=h.get("speaker", ""),
                        confidence=Confidence.HIGH,
                    )
                    self.provenance.register_source(src)
        except Exception:
            pass

        # 3. Upgrade existing tracked values from estimated → medium confidence
        # when we have corroborating real sources in the market
        n_sourced = len(seen_urls)
        if n_sourced > 0:
            for tv in self.provenance._values:
                if tv.primary_source is None:
                    tv.primary_source = SourceReference(
                        source_type=SourceType.DATABASE_SEED,
                        document_name="telecom.db",
                        confidence=Confidence.MEDIUM if n_sourced >= 3 else Confidence.LOW,
                    )

        # Track the provenance summary itself
        self.provenance.track(
            value=n_sourced,
            field_name="unique_source_urls",
            operator=self.target_operator,
        )

    def _determine_latest_period(self) -> str:
        """Find the latest calendar quarter with data for the target operator."""
        try:
            timeseries = self.db.get_financial_timeseries(
                self.target_operator, n_quarters=1
            )
            if timeseries:
                return timeseries[-1].get("calendar_quarter", "unknown")
        except Exception:
            pass

        # Fallback: direct DB query for the latest quarter
        try:
            row = self.db.conn.execute(
                "SELECT calendar_quarter FROM financial_quarterly "
                "WHERE operator_id = ? ORDER BY calendar_quarter DESC LIMIT 1",
                [self.target_operator]
            ).fetchone()
            if row:
                return row[0]
        except Exception:
            pass

        return "unknown"
