"""Market configuration registry.

To add a new market:
  1. Create a new file (e.g., uk.py) with a MarketConfig instance
  2. Import and register it in MARKET_REGISTRY below
  3. Create corresponding seed data
  4. No engine code changes needed
"""

from src.models.market_config import MarketConfig
from src.models.market_configs.germany import GERMANY_CONFIG
from src.models.market_configs.guatemala import GUATEMALA_CONFIG
from src.models.market_configs.honduras import HONDURAS_CONFIG
from src.models.market_configs.el_salvador import EL_SALVADOR_CONFIG
from src.models.market_configs.colombia import COLOMBIA_CONFIG
from src.models.market_configs.panama import PANAMA_CONFIG
from src.models.market_configs.bolivia import BOLIVIA_CONFIG
from src.models.market_configs.paraguay import PARAGUAY_CONFIG
from src.models.market_configs.nicaragua import NICARAGUA_CONFIG
from src.models.market_configs.ecuador import ECUADOR_CONFIG
from src.models.market_configs.uruguay import URUGUAY_CONFIG
from src.models.market_configs.chile import CHILE_CONFIG
from src.models.market_configs.netherlands import NETHERLANDS_CONFIG
from src.models.market_configs.belgium import BELGIUM_CONFIG
from src.models.market_configs.france import FRANCE_CONFIG
from src.models.market_configs.italy import ITALY_CONFIG
from src.models.market_configs.poland import POLAND_CONFIG
from src.models.market_configs.switzerland import SWITZERLAND_CONFIG
from src.models.market_configs.ireland import IRELAND_CONFIG
from src.models.market_configs.ukraine import UKRAINE_CONFIG
from src.models.market_configs.cyprus import CYPRUS_CONFIG
from src.models.market_configs.malta import MALTA_CONFIG

MARKET_REGISTRY: dict[str, MarketConfig] = {
    "germany": GERMANY_CONFIG,
    "guatemala": GUATEMALA_CONFIG,
    "honduras": HONDURAS_CONFIG,
    "el_salvador": EL_SALVADOR_CONFIG,
    "colombia": COLOMBIA_CONFIG,
    "panama": PANAMA_CONFIG,
    "bolivia": BOLIVIA_CONFIG,
    "paraguay": PARAGUAY_CONFIG,
    "nicaragua": NICARAGUA_CONFIG,
    "ecuador": ECUADOR_CONFIG,
    "uruguay": URUGUAY_CONFIG,
    "chile": CHILE_CONFIG,
    "netherlands": NETHERLANDS_CONFIG,
    "belgium": BELGIUM_CONFIG,
    "france": FRANCE_CONFIG,
    "italy": ITALY_CONFIG,
    "poland": POLAND_CONFIG,
    "switzerland": SWITZERLAND_CONFIG,
    "ireland": IRELAND_CONFIG,
    "ukraine": UKRAINE_CONFIG,
    "cyprus": CYPRUS_CONFIG,
    "malta": MALTA_CONFIG,
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
