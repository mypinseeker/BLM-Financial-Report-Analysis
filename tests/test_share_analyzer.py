"""Tests for src.blm.share_analyzer — Multi-Quarter Market Share Analysis."""
from __future__ import annotations

import pytest

from src.blm.share_analyzer import (
    OperatorShareSeries,
    MarketConcentration,
    ShareAnalysis,
    _extract_revenue_shares,
    _extract_subscriber_shares,
    _build_operator_series,
    _compute_hhi,
    _classify_hhi,
    _compute_ranks,
    _identify_share_movements,
    _generate_key_message,
    _classify_direction,
    compute_share_analysis,
)


# ============================================================================
# Fixtures
# ============================================================================

QUARTERS_4 = ["CQ1_2025", "CQ2_2025", "CQ3_2025", "CQ4_2025"]
QUARTERS_8 = [
    "CQ1_2024", "CQ2_2024", "CQ3_2024", "CQ4_2024",
    "CQ1_2025", "CQ2_2025", "CQ3_2025", "CQ4_2025",
]


def _make_fin_row(op_id: str, cq: str, revenue: float, name: str = "") -> dict:
    return {
        "operator_id": op_id,
        "display_name": name or op_id.replace("_", " ").title(),
        "calendar_quarter": cq,
        "total_revenue": revenue,
    }


def _make_sub_row(op_id: str, cq: str, mobile_k: float, bb_k: float = 0) -> dict:
    return {
        "operator_id": op_id,
        "calendar_quarter": cq,
        "mobile_total_k": mobile_k,
        "broadband_total_k": bb_k,
    }


def _make_market_ts_4q():
    """4-operator, 4-quarter market timeseries."""
    rows = []
    ops = [
        ("dt_germany", [3000, 3050, 3100, 3200]),
        ("vodafone_germany", [2000, 1980, 1950, 1900]),
        ("o2_germany", [1300, 1350, 1400, 1450]),
        ("oneandone_germany", [700, 720, 750, 800]),
    ]
    for op_id, revs in ops:
        for cq, rev in zip(QUARTERS_4, revs):
            rows.append(_make_fin_row(op_id, cq, rev))
    return rows


def _make_sub_data_4q():
    """4-operator subscriber data (mobile)."""
    data = {}
    ops = [
        ("dt_germany", [50000, 50500, 51000, 51500]),
        ("vodafone_germany", [30000, 29800, 29500, 29000]),
        ("o2_germany", [25000, 25500, 26000, 26500]),
        ("oneandone_germany", [10000, 10200, 10500, 10800]),
    ]
    for op_id, subs in ops:
        rows = []
        for cq, s in zip(QUARTERS_4, subs):
            rows.append(_make_sub_row(op_id, cq, s))
        data[op_id] = rows
    return data


# ============================================================================
# TestExtractRevenueShares
# ============================================================================

class TestExtractRevenueShares:
    def test_normal_4_operators(self):
        ts = _make_market_ts_4q()
        result = _extract_revenue_shares(ts, QUARTERS_4)
        assert len(result) == 4
        # Q1: DT=3000, Voda=2000, O2=1300, 1&1=700; total=7000
        assert result["dt_germany"]["CQ1_2025"] == pytest.approx(3000 / 7000 * 100, rel=1e-3)
        assert result["vodafone_germany"]["CQ1_2025"] == pytest.approx(2000 / 7000 * 100, rel=1e-3)

    def test_missing_quarter_data(self):
        # Only 2 quarters of data but ask for 4
        ts = [
            _make_fin_row("op_a", "CQ1_2025", 100),
            _make_fin_row("op_b", "CQ1_2025", 200),
            _make_fin_row("op_a", "CQ2_2025", 120),
            _make_fin_row("op_b", "CQ2_2025", 180),
        ]
        result = _extract_revenue_shares(ts, QUARTERS_4)
        # Q3, Q4 should be None for both
        assert result["op_a"]["CQ3_2025"] is None
        assert result["op_b"]["CQ4_2025"] is None

    def test_single_operator(self):
        ts = [_make_fin_row("solo", cq, 1000) for cq in QUARTERS_4]
        result = _extract_revenue_shares(ts, QUARTERS_4)
        assert len(result) == 1
        # Solo operator should have 100% share each quarter
        for cq in QUARTERS_4:
            assert result["solo"][cq] == pytest.approx(100.0)

    def test_empty_timeseries(self):
        result = _extract_revenue_shares([], QUARTERS_4)
        assert result == {}


# ============================================================================
# TestExtractSubscriberShares
# ============================================================================

class TestExtractSubscriberShares:
    def test_normal_mobile(self):
        sub_data = _make_sub_data_4q()
        result = _extract_subscriber_shares(sub_data, QUARTERS_4, "mobile_total_k")
        assert len(result) == 4
        # Q1 total: 50000+30000+25000+10000 = 115000
        assert result["dt_germany"]["CQ1_2025"] == pytest.approx(50000 / 115000 * 100, rel=1e-3)

    def test_missing_field_returns_none(self):
        sub_data = {
            "op_a": [{"operator_id": "op_a", "calendar_quarter": "CQ1_2025", "mobile_total_k": 1000}],
            "op_b": [{"operator_id": "op_b", "calendar_quarter": "CQ1_2025"}],  # No mobile_total_k
        }
        result = _extract_subscriber_shares(sub_data, ["CQ1_2025"], "mobile_total_k")
        assert result["op_a"]["CQ1_2025"] == pytest.approx(100.0)
        assert result["op_b"]["CQ1_2025"] is None

    def test_empty_sub_data(self):
        result = _extract_subscriber_shares({}, QUARTERS_4, "mobile_total_k")
        assert result == {}


# ============================================================================
# TestBuildOperatorSeries
# ============================================================================

class TestBuildOperatorSeries:
    def test_gaining_operator(self):
        shares = {"CQ1_2025": 40.0, "CQ2_2025": 41.0, "CQ3_2025": 42.0, "CQ4_2025": 43.0}
        ranks = {"CQ1_2025": 1, "CQ2_2025": 1, "CQ3_2025": 1, "CQ4_2025": 1}
        s = _build_operator_series("dt", "Deutsche Telekom", shares, QUARTERS_4, ranks)
        assert s.direction == "gaining"
        assert s.share_change_pp == pytest.approx(3.0)
        assert s.avg_quarterly_change_pp == pytest.approx(1.0)
        assert s.rank_latest == 1
        assert s.rank_change == 0

    def test_losing_operator(self):
        shares = {"CQ1_2025": 30.0, "CQ2_2025": 29.0, "CQ3_2025": 28.0, "CQ4_2025": 27.0}
        ranks = {"CQ1_2025": 2, "CQ2_2025": 2, "CQ3_2025": 3, "CQ4_2025": 3}
        s = _build_operator_series("voda", "Vodafone", shares, QUARTERS_4, ranks)
        assert s.direction == "losing"
        assert s.share_change_pp == pytest.approx(-3.0)
        assert s.rank_change == -1  # Dropped from 2 to 3

    def test_stable_operator(self):
        shares = {"CQ1_2025": 20.0, "CQ2_2025": 20.1, "CQ3_2025": 19.9, "CQ4_2025": 20.0}
        ranks = {"CQ1_2025": 3, "CQ2_2025": 3, "CQ3_2025": 3, "CQ4_2025": 3}
        s = _build_operator_series("o2", "O2", shares, QUARTERS_4, ranks)
        assert s.direction == "stable"

    def test_insufficient_data(self):
        shares = {"CQ1_2025": None, "CQ2_2025": None, "CQ3_2025": None, "CQ4_2025": 25.0}
        ranks = {"CQ4_2025": 2}
        s = _build_operator_series("op", "Op", shares, QUARTERS_4, ranks)
        assert s.latest_share_pct == 25.0
        assert s.share_change_pp is None  # Only 1 valid point
        assert s.direction == "stable"


# ============================================================================
# TestComputeHHI
# ============================================================================

class TestComputeHHI:
    def test_monopoly(self):
        shares = {"CQ1": [100.0]}
        result = _compute_hhi(shares)
        assert result == [10000.0]

    def test_duopoly(self):
        shares = {"CQ1": [50.0, 50.0]}
        result = _compute_hhi(shares)
        assert result[0] == pytest.approx(5000.0)

    def test_competitive(self):
        # 4 equal operators at 25% each
        shares = {"CQ1": [25.0, 25.0, 25.0, 25.0]}
        result = _compute_hhi(shares)
        assert result[0] == pytest.approx(2500.0)

    def test_empty(self):
        shares = {"CQ1": []}
        result = _compute_hhi(shares)
        assert result == [0.0]


# ============================================================================
# TestClassifyHHI
# ============================================================================

class TestClassifyHHI:
    def test_highly_concentrated(self):
        assert _classify_hhi(3000) == "highly_concentrated"
        assert _classify_hhi(2500) == "highly_concentrated"

    def test_moderately_concentrated(self):
        assert _classify_hhi(2000) == "moderately_concentrated"
        assert _classify_hhi(1500) == "moderately_concentrated"

    def test_competitive(self):
        assert _classify_hhi(1200) == "competitive"
        assert _classify_hhi(0) == "competitive"


# ============================================================================
# TestComputeRanks
# ============================================================================

class TestComputeRanks:
    def test_normal_ranking(self):
        shares = {
            "op_a": {"CQ1": 50.0, "CQ2": 45.0},
            "op_b": {"CQ1": 30.0, "CQ2": 35.0},
            "op_c": {"CQ1": 20.0, "CQ2": 20.0},
        }
        ranks = _compute_ranks(shares, ["CQ1", "CQ2"])
        assert ranks["op_a"]["CQ1"] == 1
        assert ranks["op_b"]["CQ1"] == 2
        assert ranks["op_c"]["CQ1"] == 3
        # Q2: a dropped, b gained
        assert ranks["op_a"]["CQ2"] == 1
        assert ranks["op_b"]["CQ2"] == 2

    def test_ties(self):
        shares = {
            "op_a": {"CQ1": 50.0},
            "op_b": {"CQ1": 50.0},
        }
        ranks = _compute_ranks(shares, ["CQ1"])
        # Both at 50%, rank order is deterministic but both are in top 2
        assert set([ranks["op_a"]["CQ1"], ranks["op_b"]["CQ1"]]) == {1, 2}

    def test_single_quarter(self):
        shares = {"op_a": {"CQ1": 100.0}}
        ranks = _compute_ranks(shares, ["CQ1"])
        assert ranks["op_a"]["CQ1"] == 1


# ============================================================================
# TestIdentifyMovements
# ============================================================================

class TestIdentifyMovements:
    def test_clear_gainer_loser(self):
        series = [
            OperatorShareSeries(operator_id="a", share_change_pp=3.0),
            OperatorShareSeries(operator_id="b", share_change_pp=-2.0),
            OperatorShareSeries(operator_id="c", share_change_pp=0.5),
        ]
        gainer, loser = _identify_share_movements(series)
        assert gainer == "a"
        assert loser == "b"

    def test_all_stable(self):
        series = [
            OperatorShareSeries(operator_id="a", share_change_pp=0.05),
            OperatorShareSeries(operator_id="b", share_change_pp=-0.03),
        ]
        gainer, loser = _identify_share_movements(series)
        assert gainer is None
        assert loser is None

    def test_single_operator(self):
        series = [OperatorShareSeries(operator_id="a", share_change_pp=2.0)]
        gainer, loser = _identify_share_movements(series)
        assert gainer == "a"
        assert loser is None


# ============================================================================
# TestGenerateKeyMessage
# ============================================================================

class TestGenerateKeyMessage:
    def test_gaining_target(self):
        target = OperatorShareSeries(
            operator_id="voda", direction="gaining",
            latest_share_pct=28.5, share_change_pp=1.5, rank_latest=2,
        )
        conc = MarketConcentration(hhi=2800, hhi_label="highly_concentrated",
                                   hhi_direction="concentrating")
        msg = _generate_key_message(target, conc, "revenue")
        assert "28.5%" in msg
        assert "#2" in msg
        assert "gaining" in msg
        assert "+1.5pp" in msg
        assert "highly concentrated" in msg

    def test_losing_target(self):
        target = OperatorShareSeries(
            operator_id="voda", direction="losing",
            latest_share_pct=25.0, share_change_pp=-2.0, rank_latest=3,
        )
        conc = MarketConcentration(hhi=1800, hhi_label="moderately_concentrated",
                                   hhi_direction="stable")
        msg = _generate_key_message(target, conc, "mobile_subscribers")
        assert "losing" in msg
        assert "-2.0pp" in msg

    def test_no_target(self):
        conc = MarketConcentration(hhi=1200, hhi_label="competitive",
                                   hhi_direction="stable")
        msg = _generate_key_message(None, conc, "revenue")
        assert "unavailable" in msg


# ============================================================================
# TestComputeShareAnalysis (orchestrator)
# ============================================================================

class TestComputeShareAnalysis:
    def test_full_4q_revenue(self):
        ts = _make_market_ts_4q()
        names = {
            "dt_germany": "Deutsche Telekom",
            "vodafone_germany": "Vodafone",
            "o2_germany": "O2",
            "oneandone_germany": "1&1",
        }
        sa = compute_share_analysis(
            market_ts=ts, sub_data_by_op={}, quarters=QUARTERS_4,
            target_operator_id="vodafone_germany", metric_type="revenue",
            display_names=names,
        )
        assert sa.metric_type == "revenue"
        assert len(sa.operator_series) == 4
        assert sa.target_series is not None
        assert sa.target_series.operator_id == "vodafone_germany"
        assert sa.target_series.direction == "losing"
        assert sa.share_leader_id == "dt_germany"
        assert sa.concentration.hhi > 0
        assert sa.key_message  # Non-empty

    def test_full_4q_mobile_subscribers(self):
        sub_data = _make_sub_data_4q()
        sa = compute_share_analysis(
            market_ts=[], sub_data_by_op=sub_data, quarters=QUARTERS_4,
            target_operator_id="vodafone_germany",
            metric_type="mobile_subscribers",
        )
        assert sa.metric_type == "mobile_subscribers"
        assert len(sa.operator_series) == 4
        assert sa.target_series is not None

    def test_minimal_data(self):
        ts = [
            _make_fin_row("op_a", "CQ1_2025", 100),
            _make_fin_row("op_b", "CQ1_2025", 200),
        ]
        sa = compute_share_analysis(
            market_ts=ts, sub_data_by_op={}, quarters=["CQ1_2025"],
            target_operator_id="op_a", metric_type="revenue",
        )
        assert len(sa.operator_series) == 2
        assert sa.target_series is not None
        assert sa.target_series.latest_share_pct == pytest.approx(33.33, rel=1e-2)

    def test_single_operator(self):
        ts = [_make_fin_row("solo", cq, 500) for cq in QUARTERS_4]
        sa = compute_share_analysis(
            market_ts=ts, sub_data_by_op={}, quarters=QUARTERS_4,
            target_operator_id="solo", metric_type="revenue",
        )
        assert len(sa.operator_series) == 1
        assert sa.target_series.latest_share_pct == pytest.approx(100.0)
        assert sa.concentration.hhi == pytest.approx(10000.0)

    def test_empty_quarters(self):
        sa = compute_share_analysis(
            market_ts=[], sub_data_by_op={}, quarters=[],
            target_operator_id="x", metric_type="revenue",
        )
        assert sa.operator_series == []
        assert sa.target_series is None

    def test_to_dict_serialization(self):
        ts = _make_market_ts_4q()
        sa = compute_share_analysis(
            market_ts=ts, sub_data_by_op={}, quarters=QUARTERS_4,
            target_operator_id="vodafone_germany", metric_type="revenue",
        )
        d = sa.to_dict()
        assert isinstance(d, dict)
        assert d["metric_type"] == "revenue"
        assert isinstance(d["operator_series"], list)
        assert isinstance(d["concentration"], dict)
        assert "hhi" in d["concentration"]


# ============================================================================
# TestEdgeCases
# ============================================================================

class TestEdgeCases:
    def test_zero_revenue_quarter(self):
        ts = [
            _make_fin_row("op_a", "CQ1_2025", 0),
            _make_fin_row("op_b", "CQ1_2025", 0),
            _make_fin_row("op_a", "CQ2_2025", 100),
            _make_fin_row("op_b", "CQ2_2025", 200),
        ]
        result = _extract_revenue_shares(ts, ["CQ1_2025", "CQ2_2025"])
        # Q1 has zero total → shares should be None
        assert result["op_a"]["CQ1_2025"] is None
        assert result["op_b"]["CQ1_2025"] is None
        # Q2 is normal
        assert result["op_a"]["CQ2_2025"] == pytest.approx(100 / 300 * 100, rel=1e-3)

    def test_one_quarter_only(self):
        ts = [_make_fin_row("a", "CQ4_2025", 500), _make_fin_row("b", "CQ4_2025", 500)]
        sa = compute_share_analysis(
            market_ts=ts, sub_data_by_op={}, quarters=["CQ4_2025"],
            target_operator_id="a", metric_type="revenue",
        )
        assert sa.target_series.latest_share_pct == pytest.approx(50.0)
        assert sa.target_series.share_change_pp is None  # Only 1 quarter
        assert sa.target_series.direction == "stable"

    def test_operator_appears_mid_series(self):
        """Operator only has data for later quarters."""
        ts = [
            _make_fin_row("old", "CQ1_2025", 1000),
            _make_fin_row("old", "CQ2_2025", 1000),
            _make_fin_row("old", "CQ3_2025", 900),
            _make_fin_row("old", "CQ4_2025", 800),
            # 'new' only appears from Q3
            _make_fin_row("new", "CQ3_2025", 100),
            _make_fin_row("new", "CQ4_2025", 200),
        ]
        result = _extract_revenue_shares(ts, QUARTERS_4)
        assert result["new"]["CQ1_2025"] is None
        assert result["new"]["CQ2_2025"] is None
        assert result["new"]["CQ3_2025"] is not None
        assert result["new"]["CQ4_2025"] is not None


# ============================================================================
# TestClassifyDirection
# ============================================================================

class TestClassifyDirection:
    def test_gaining(self):
        assert _classify_direction(1.0) == "gaining"
        assert _classify_direction(0.51) == "gaining"

    def test_losing(self):
        assert _classify_direction(-1.0) == "losing"
        assert _classify_direction(-0.51) == "losing"

    def test_stable(self):
        assert _classify_direction(0.0) == "stable"
        assert _classify_direction(0.5) == "stable"
        assert _classify_direction(-0.5) == "stable"
        assert _classify_direction(None) == "stable"
