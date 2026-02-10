"""BLM Financial Report Analysis Tool."""

__version__ = "0.1.0"

# Heavy imports (pandas, matplotlib, Config, DataLoader, etc.) are NOT loaded
# eagerly here — they are only needed by the analysis CLI, not the web app.
# Import them directly where needed:
#   from src.config import Config
#   from src.data.loader import DataLoader
#   etc.
