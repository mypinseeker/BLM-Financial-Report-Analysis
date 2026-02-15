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

# Legacy imports are lazy-loaded to avoid pulling in numpy/matplotlib
# in slim deployments (Vercel Lambda). Access legacy symbols via
# src.blm._legacy directly, or they'll be resolved on first access here.

_LEGACY_NAMES = {
    "GLOBAL_OPERATORS", "BUSINESS_SEGMENTS", "COMPETITIVE_DIMENSIONS",
    "OperatorProfile", "MarketContext", "TelecomDataGenerator",
    "generate_sample_data", "InsightResult", "FiveLooksAnalyzer",
    "StrategyItem", "StrategyResult", "ThreeDecisionsEngine",
    "generate_blm_strategy", "BLMReportGenerator", "blm_cli",
    "BLMPPTGenerator", "PPTStyle", "HUAWEI_STYLE", "VODAFONE_STYLE",
    "generate_blm_ppt", "BLMPPTGeneratorEnhanced",
    "generate_enhanced_blm_ppt", "PPTChartGenerator", "PPT_AVAILABLE",
    "CanvaBLMExporter", "check_canva_credentials",
}


def __getattr__(name):
    if name in _LEGACY_NAMES:
        import src.blm._legacy as _legacy
        try:
            return getattr(_legacy, name)
        except AttributeError:
            pass
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = list(_LEGACY_NAMES)
