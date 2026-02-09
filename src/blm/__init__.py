"""BLM (Business Leadership Model) Strategic Analysis Engine.

Phase 1 restructured architecture:
- New: src/blm/engine.py (BLMAnalysisEngine)
- New: src/blm/look_at_*.py (five looks analysis modules)
- New: src/blm/swot_synthesis.py (SWOT bridge analysis)
- Legacy: src/blm/_legacy/ (original implementations, preserved)

Usage (new):
    from src.database.db import TelecomDatabase
    from src.blm.engine import BLMAnalysisEngine

    db = TelecomDatabase("data/telecom.db")
    engine = BLMAnalysisEngine(db, target_operator="vodafone_germany", market="germany")
    result = engine.run_five_looks()

Usage (legacy, backward-compatible):
    from src.blm._legacy import generate_blm_strategy, generate_sample_data
"""

# Legacy backward compatibility — import from _legacy for old code paths
from src.blm._legacy import (
    GLOBAL_OPERATORS,
    BUSINESS_SEGMENTS,
    COMPETITIVE_DIMENSIONS,
    OperatorProfile,
    MarketContext,
    TelecomDataGenerator,
    generate_sample_data,
    InsightResult,
    FiveLooksAnalyzer,
    StrategyItem,
    StrategyResult,
    ThreeDecisionsEngine,
    generate_blm_strategy,
    BLMReportGenerator,
    blm_cli,
)

try:
    from src.blm._legacy import (
        BLMPPTGenerator,
        PPTStyle,
        HUAWEI_STYLE,
        VODAFONE_STYLE,
        generate_blm_ppt,
        BLMPPTGeneratorEnhanced,
        generate_enhanced_blm_ppt,
        PPTChartGenerator,
        PPT_AVAILABLE,
    )
except (ImportError, AttributeError):
    PPT_AVAILABLE = False

from src.blm._legacy import (
    CanvaBLMExporter,
    check_canva_credentials,
)

__all__ = [
    # Legacy exports
    "GLOBAL_OPERATORS",
    "BUSINESS_SEGMENTS",
    "COMPETITIVE_DIMENSIONS",
    "OperatorProfile",
    "MarketContext",
    "TelecomDataGenerator",
    "generate_sample_data",
    "InsightResult",
    "FiveLooksAnalyzer",
    "StrategyItem",
    "StrategyResult",
    "ThreeDecisionsEngine",
    "generate_blm_strategy",
    "BLMReportGenerator",
    "blm_cli",
    "PPT_AVAILABLE",
    "CanvaBLMExporter",
    "check_canva_credentials",
]
