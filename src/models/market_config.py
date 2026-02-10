"""MarketConfig — market-specific configuration for BLM analysis engine.

Each telecom market defines a MarketConfig that encapsulates all
market-specific parameters. The engine reads config values instead of
hardcoding any market-specific data.

To add a new market:
  1. Create src/models/market_configs/<market>.py with a MarketConfig instance
  2. Register it in src/models/market_configs/__init__.py
  3. Create seed data (operators + financials + tariffs)
  4. No engine code changes needed
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MarketConfig:
    """Market-specific configuration for BLM analysis engine."""

    # --- Identity ---
    market_id: str              # "germany", "uk", "japan"
    market_name: str            # "Germany", "United Kingdom", "Japan"
    country: str                # Country name for macro_environment table
    currency: str               # "EUR", "GBP", "JPY"
    currency_symbol: str        # "€", "£", "¥"
    regulatory_body: str        # "BNetzA", "Ofcom", "MIC"
    population_k: float         # Population in thousands (for penetration calcs)

    # --- Customer Segments ---
    # List of dicts: {segment_name, segment_type, unmet_needs, pain_points, purchase_decision_factors}
    customer_segments: list[dict] = field(default_factory=list)

    # --- Operator BMC Enrichments ---
    # operator_id → {key_resources: [...], value_propositions: [...], key_partners: [...], key_activities: [...]}
    operator_bmc_enrichments: dict[str, dict] = field(default_factory=dict)

    # --- Operator Exposure Points ---
    # operator_id → [{trigger_action, side_effect, attack_vector, severity, evidence}]
    operator_exposures: dict[str, list[dict]] = field(default_factory=dict)

    # --- Competitive Landscape ---
    competitive_landscape_notes: list[str] = field(default_factory=list)

    # --- PEST Context ---
    # {political: [...], economic: [...], social: [...], technological: [...]}
    pest_context: dict = field(default_factory=dict)
