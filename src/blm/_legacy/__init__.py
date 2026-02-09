"""Legacy BLM modules — preserved for backward compatibility.

All original src/blm/*.py files have been moved here during the Phase 1 restructure.
Import from here if you need access to the original implementations.
"""

from src.blm._legacy.telecom_data import (
    GLOBAL_OPERATORS,
    BUSINESS_SEGMENTS,
    COMPETITIVE_DIMENSIONS,
    OperatorProfile,
    MarketContext,
    TelecomDataGenerator,
    generate_sample_data,
)

from src.blm._legacy.five_looks import (
    InsightResult,
    FiveLooksAnalyzer,
)

from src.blm._legacy.three_decisions import (
    StrategyItem,
    StrategyResult,
    ThreeDecisionsEngine,
    generate_blm_strategy,
)

from src.blm._legacy.report_generator import BLMReportGenerator

from src.blm._legacy.cli import blm_cli

try:
    from src.blm._legacy.ppt_generator import (
        BLMPPTGenerator,
        PPTStyle,
        HUAWEI_STYLE,
        VODAFONE_STYLE,
        generate_blm_ppt,
    )
    from src.blm._legacy.ppt_generator_enhanced import (
        BLMPPTGeneratorEnhanced,
        generate_enhanced_blm_ppt,
    )
    from src.blm._legacy.ppt_charts import PPTChartGenerator
    PPT_AVAILABLE = True
except ImportError:
    PPT_AVAILABLE = False

from src.blm._legacy.canva_integration import (
    CanvaBLMExporter,
    check_canva_credentials,
)
