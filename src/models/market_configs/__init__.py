"""Market configuration registry.

To add a new market:
  1. Create a new file (e.g., uk.py) with a MarketConfig instance
  2. Import and register it in MARKET_REGISTRY below
  3. Create corresponding seed data
  4. No engine code changes needed
"""

from src.models.market_config import MarketConfig
from src.models.market_configs.germany import GERMANY_CONFIG

MARKET_REGISTRY: dict[str, MarketConfig] = {
    "germany": GERMANY_CONFIG,
}


def get_market_config(market_id: str) -> MarketConfig:
    """Get the MarketConfig for a given market ID.

    Args:
        market_id: Market identifier (e.g., "germany", "uk")

    Returns:
        MarketConfig instance for the market

    Raises:
        ValueError: If market_id is not registered
    """
    if market_id not in MARKET_REGISTRY:
        available = list(MARKET_REGISTRY.keys())
        raise ValueError(
            f"Unknown market: '{market_id}'. Available markets: {available}"
        )
    return MARKET_REGISTRY[market_id]
