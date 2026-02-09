"""Universal telecom operator data model for BLM strategic analysis.

Supports any global telecom operator with flexible data structures.
Includes sample data generation for major global operators.
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import pandas as pd


# ============================================================================
# Global Operator Registry - can be extended with any operator
# ============================================================================

GLOBAL_OPERATORS = {
    # China
    "China Mobile": {"country": "China", "region": "APAC", "type": "incumbent"},
    "China Telecom": {"country": "China", "region": "APAC", "type": "incumbent"},
    "China Unicom": {"country": "China", "region": "APAC", "type": "incumbent"},
    # Europe
    "Vodafone": {"country": "UK", "region": "Europe", "type": "multinational"},
    "Deutsche Telekom": {"country": "Germany", "region": "Europe", "type": "incumbent"},
    "Orange": {"country": "France", "region": "Europe", "type": "multinational"},
    "Telefonica": {"country": "Spain", "region": "Europe", "type": "multinational"},
    "BT Group": {"country": "UK", "region": "Europe", "type": "incumbent"},
    # Americas
    "AT&T": {"country": "USA", "region": "Americas", "type": "incumbent"},
    "Verizon": {"country": "USA", "region": "Americas", "type": "incumbent"},
    "T-Mobile US": {"country": "USA", "region": "Americas", "type": "challenger"},
    "America Movil": {"country": "Mexico", "region": "Americas", "type": "multinational"},
    # Africa & Middle East
    "MTN": {"country": "South Africa", "region": "Africa", "type": "multinational"},
    "Airtel Africa": {"country": "India/Africa", "region": "Africa", "type": "multinational"},
    "Etisalat": {"country": "UAE", "region": "MEA", "type": "incumbent"},
    "STC": {"country": "Saudi Arabia", "region": "MEA", "type": "incumbent"},
    # Asia Pacific
    "NTT Docomo": {"country": "Japan", "region": "APAC", "type": "incumbent"},
    "SoftBank": {"country": "Japan", "region": "APAC", "type": "challenger"},
    "SK Telecom": {"country": "South Korea", "region": "APAC", "type": "incumbent"},
    "Singtel": {"country": "Singapore", "region": "APAC", "type": "incumbent"},
    "Telstra": {"country": "Australia", "region": "APAC", "type": "incumbent"},
    "Reliance Jio": {"country": "India", "region": "APAC", "type": "disruptor"},
    "Bharti Airtel": {"country": "India", "region": "APAC", "type": "incumbent"},
}

BUSINESS_SEGMENTS = [
    "Mobile Services",
    "Fixed Broadband",
    "Enterprise/B2B",
    "Digital Services",
    "Cloud & IT",
    "IoT",
    "Data Center",
    "FinTech/Mobile Money",
]

COMPETITIVE_DIMENSIONS = [
    "Network Coverage",
    "Network Quality",
    "Brand Strength",
    "Channel Capability",
    "Price Competitiveness",
    "Enterprise Capability",
    "Innovation",
    "Customer Service",
    "Digital Capability",
    "Ecosystem & Partners",
]


@dataclass
class OperatorProfile:
    """Profile of a telecom operator for analysis."""
    name: str
    country: str
    region: str
    operator_type: str  # incumbent, challenger, disruptor, multinational
    market_position: int = 1  # 1=leader, 2=challenger, 3=follower
    founded_year: Optional[int] = None

    @classmethod
    def from_registry(cls, name: str) -> "OperatorProfile":
        if name in GLOBAL_OPERATORS:
            info = GLOBAL_OPERATORS[name]
            return cls(
                name=name,
                country=info["country"],
                region=info["region"],
                operator_type=info["type"],
            )
        raise ValueError(f"Unknown operator: {name}. Add to GLOBAL_OPERATORS or create manually.")


@dataclass
class MarketContext:
    """Market context for analysis - supports multi-country scenarios."""
    countries: list[str]
    analysis_period: str  # e.g., "2023Q1-2024Q4"
    target_operator: str  # The operator being analyzed
    competitors: list[str]  # Competitors to compare against
    currency: str = "USD"


# ============================================================================
# Sample Data Generator - generates realistic data for any operator set
# ============================================================================

class TelecomDataGenerator:
    """Generate sample telecom operator data for BLM analysis."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)

    def generate_dataset(
        self,
        operators: list[str],
        n_quarters: int = 8,
        base_year: int = 2023,
    ) -> dict[str, pd.DataFrame]:
        """Generate complete dataset for specified operators.

        Args:
            operators: List of operator names to generate data for.
            n_quarters: Number of quarters of data.
            base_year: Starting year.

        Returns:
            Dict with DataFrames: market, financial, competitive, macro, segments
        """
        quarters = self._quarter_labels(n_quarters, base_year)

        return {
            "market": self._gen_market_data(operators, quarters),
            "financial": self._gen_financial_data(operators, quarters),
            "competitive": self._gen_competitive_data(operators, quarters),
            "macro": self._gen_macro_data(operators, quarters),
            "segments": self._gen_segment_data(operators, quarters),
            "customer": self._gen_customer_data(operators, quarters),
        }

    def _quarter_labels(self, n: int, base_year: int) -> list[str]:
        labels = []
        for i in range(n):
            q = i % 4 + 1
            y = base_year + i // 4
            labels.append(f"{y}Q{q}")
        return labels

    def _get_operator_scale(self, op: str) -> dict:
        """Get scale factors based on operator size."""
        # Revenue in billions USD, subscribers in millions
        scales = {
            "China Mobile": {"revenue": 35, "subs": 980, "margin": 0.12},
            "China Telecom": {"revenue": 18, "subs": 400, "margin": 0.09},
            "China Unicom": {"revenue": 13, "subs": 320, "margin": 0.06},
            "Vodafone": {"revenue": 12, "subs": 300, "margin": 0.08},
            "Deutsche Telekom": {"revenue": 30, "subs": 250, "margin": 0.10},
            "Orange": {"revenue": 11, "subs": 280, "margin": 0.09},
            "Telefonica": {"revenue": 10, "subs": 380, "margin": 0.07},
            "AT&T": {"revenue": 30, "subs": 200, "margin": 0.11},
            "Verizon": {"revenue": 33, "subs": 145, "margin": 0.14},
            "T-Mobile US": {"revenue": 20, "subs": 120, "margin": 0.10},
            "MTN": {"revenue": 4.5, "subs": 280, "margin": 0.18},
            "Airtel Africa": {"revenue": 1.5, "subs": 140, "margin": 0.22},
            "Reliance Jio": {"revenue": 6, "subs": 450, "margin": 0.15},
            "Bharti Airtel": {"revenue": 4, "subs": 350, "margin": 0.12},
        }
        return scales.get(op, {"revenue": 5, "subs": 50, "margin": 0.08})

    def _gen_market_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        rows = []
        for i, q in enumerate(quarters):
            # Calculate total market for share calculation
            total_subs = sum(self._get_operator_scale(op)["subs"] for op in operators)
            for op in operators:
                scale = self._get_operator_scale(op)
                base_subs = scale["subs"]
                growth = 1 + self.rng.uniform(0.005, 0.02) * (i + 1)
                subs = base_subs * growth + self.rng.normal(0, base_subs * 0.01)
                rows.append({
                    "quarter": q,
                    "operator": op,
                    "subscribers_million": round(subs, 1),
                    "market_share_pct": round(subs / total_subs * 100, 1),
                    "4g_users_pct": round(min(95, 70 + i * 2 + self.rng.normal(0, 2)), 1),
                    "5g_users_pct": round(min(60, 15 + i * 5 + self.rng.normal(0, 3)), 1),
                    "broadband_users_million": round(subs * self.rng.uniform(0.15, 0.35), 1),
                    "net_adds_million": round(self.rng.uniform(-0.5, 2.0) * base_subs / 100, 2),
                    "churn_rate_pct": round(self.rng.uniform(0.8, 2.5), 2),
                })
        return pd.DataFrame(rows)

    def _gen_financial_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        rows = []
        for i, q in enumerate(quarters):
            for op in operators:
                scale = self._get_operator_scale(op)
                growth = 1 + self.rng.uniform(0.01, 0.03) * (i + 1) * 0.3
                revenue = scale["revenue"] * growth + self.rng.normal(0, scale["revenue"] * 0.02)
                margin = scale["margin"] + self.rng.normal(0, 0.005)
                rows.append({
                    "quarter": q,
                    "operator": op,
                    "revenue_billion_usd": round(revenue, 2),
                    "ebitda_billion_usd": round(revenue * (margin + 0.2), 2),
                    "net_profit_billion_usd": round(revenue * margin, 2),
                    "profit_margin_pct": round(margin * 100, 1),
                    "ebitda_margin_pct": round((margin + 0.2) * 100, 1),
                    "capex_billion_usd": round(revenue * self.rng.uniform(0.12, 0.22), 2),
                    "capex_to_revenue_pct": round(self.rng.uniform(12, 22), 1),
                    "arpu_usd": round(self.rng.uniform(5, 45), 1),
                    "revenue_growth_yoy_pct": round((growth - 1) * 100 + self.rng.normal(0, 1), 1),
                    "opex_efficiency_pct": round(self.rng.uniform(1, 4), 1),
                })
        return pd.DataFrame(rows)

    def _gen_competitive_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        # Base competitive scores (can be customized per operator)
        base_scores = {
            "China Mobile": {"Network Coverage": 95, "Network Quality": 90, "Brand Strength": 92,
                            "Price Competitiveness": 70, "Enterprise Capability": 85, "Innovation": 80},
            "Vodafone": {"Network Coverage": 85, "Network Quality": 82, "Brand Strength": 88,
                        "Price Competitiveness": 75, "Enterprise Capability": 90, "Innovation": 85},
            "MTN": {"Network Coverage": 80, "Network Quality": 75, "Brand Strength": 85,
                   "Price Competitiveness": 80, "Enterprise Capability": 70, "Innovation": 75},
        }
        rows = []
        for i, q in enumerate(quarters):
            for op in operators:
                op_scores = base_scores.get(op, {dim: 75 for dim in COMPETITIVE_DIMENSIONS})
                for dim in COMPETITIVE_DIMENSIONS:
                    base = op_scores.get(dim, 75)
                    score = base + self.rng.normal(0, 2) + i * self.rng.uniform(-0.3, 0.5)
                    rows.append({
                        "quarter": q,
                        "operator": op,
                        "dimension": dim,
                        "score": round(min(100, max(0, score)), 1),
                    })
        return pd.DataFrame(rows)

    def _gen_macro_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        # Get unique countries from operators
        countries = list(set(
            GLOBAL_OPERATORS.get(op, {}).get("country", "Unknown")
            for op in operators
        ))
        rows = []
        for i, q in enumerate(quarters):
            for country in countries:
                rows.append({
                    "quarter": q,
                    "country": country,
                    "gdp_growth_pct": round(self.rng.uniform(1, 6), 1),
                    "inflation_pct": round(self.rng.uniform(2, 8), 1),
                    "telecom_penetration_pct": round(min(130, 90 + i * 1.5 + self.rng.normal(0, 2)), 1),
                    "5g_coverage_pct": round(min(85, 20 + i * 6 + self.rng.normal(0, 3)), 1),
                    "digital_economy_pct": round(min(50, 25 + i * 2 + self.rng.normal(0, 1)), 1),
                    "regulatory_index": round(self.rng.uniform(60, 90), 0),
                    "competitive_intensity": self.rng.choice(["High", "Medium", "Low"], p=[0.4, 0.4, 0.2]),
                })
        return pd.DataFrame(rows)

    def _gen_segment_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        # Base segment mix varies by operator type
        segment_mix = {
            "Mobile Services": 50, "Fixed Broadband": 15, "Enterprise/B2B": 18,
            "Digital Services": 6, "Cloud & IT": 5, "IoT": 3,
            "Data Center": 2, "FinTech/Mobile Money": 1,
        }
        rows = []
        for i, q in enumerate(quarters):
            for op in operators:
                for seg in BUSINESS_SEGMENTS:
                    base = segment_mix[seg]
                    # New digital segments grow faster
                    is_growth = seg in ("Digital Services", "Cloud & IT", "IoT", "FinTech/Mobile Money")
                    growth = self.rng.uniform(0.08, 0.20) if is_growth else self.rng.uniform(-0.02, 0.04)
                    pct = base * (1 + growth * i * 0.5)
                    rows.append({
                        "quarter": q,
                        "operator": op,
                        "segment": seg,
                        "revenue_share_pct": round(pct, 1),
                        "yoy_growth_pct": round(growth * 100 * (1 + i * 0.1), 1),
                        "is_growth_segment": is_growth,
                    })
        return pd.DataFrame(rows)

    def _gen_customer_data(self, operators: list[str], quarters: list[str]) -> pd.DataFrame:
        rows = []
        for i, q in enumerate(quarters):
            for op in operators:
                rows.append({
                    "quarter": q,
                    "operator": op,
                    "nps_score": round(self.rng.uniform(20, 55), 0),
                    "csat_score": round(self.rng.uniform(70, 88), 1),
                    "digital_engagement_pct": round(min(80, 40 + i * 3 + self.rng.normal(0, 2)), 1),
                    "app_mau_million": round(self.rng.uniform(10, 100), 1),
                    "self_service_pct": round(min(70, 35 + i * 3 + self.rng.normal(0, 2)), 1),
                    "complaint_rate_per_1000": round(self.rng.uniform(2, 15), 1),
                })
        return pd.DataFrame(rows)


def generate_sample_data(
    operators: list[str] = None,
    n_quarters: int = 8,
    seed: int = 42,
) -> dict[str, pd.DataFrame]:
    """Convenience function to generate sample data.

    Args:
        operators: List of operator names. Defaults to China Big 3.
        n_quarters: Number of quarters of data.
        seed: Random seed for reproducibility.

    Returns:
        Dict of DataFrames with market, financial, competitive, macro, segments, customer data.
    """
    if operators is None:
        operators = ["China Mobile", "China Telecom", "China Unicom"]
    generator = TelecomDataGenerator(seed=seed)
    return generator.generate_dataset(operators, n_quarters)
