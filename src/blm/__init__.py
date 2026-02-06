"""BLM (Business Leadership Model) Strategic Analysis Skill.

A universal framework for telecom operator strategic analysis supporting:
- Five Looks (五看): Market, Self, Competitor, Macro, Opportunity insights
- Three Decisions (三定): Strategy, Key Tasks, Execution planning
- Multi-operator comparison across any market

Supports global operators: Vodafone, MTN, Orange, Telefonica, China Mobile,
AT&T, Verizon, Deutsche Telekom, and many more.

Usage:
    from src.blm import generate_blm_strategy, generate_sample_data

    # Generate sample data for operators
    data = generate_sample_data(["Vodafone", "MTN", "Orange"])

    # Run full BLM analysis
    results = generate_blm_strategy(data, "Vodafone", ["MTN", "Orange"])

    # Access Five Looks insights
    market_insight = results["five_looks"]["market"]

    # Access Three Decisions strategy
    strategy = results["three_decisions"]["strategy"]
"""

from src.blm.telecom_data import (
    GLOBAL_OPERATORS,
    BUSINESS_SEGMENTS,
    COMPETITIVE_DIMENSIONS,
    OperatorProfile,
    MarketContext,
    TelecomDataGenerator,
    generate_sample_data,
)

from src.blm.five_looks import (
    InsightResult,
    FiveLooksAnalyzer,
)

from src.blm.three_decisions import (
    StrategyItem,
    StrategyResult,
    ThreeDecisionsEngine,
    generate_blm_strategy,
)

from src.blm.report_generator import BLMReportGenerator

from src.blm.cli import blm_cli

# Optional PPT generation (requires python-pptx)
try:
    from src.blm.ppt_generator import (
        BLMPPTGenerator,
        PPTStyle,
        HUAWEI_STYLE,
        VODAFONE_STYLE,
        generate_blm_ppt,
    )
    from src.blm.ppt_generator_enhanced import (
        BLMPPTGeneratorEnhanced,
        generate_enhanced_blm_ppt,
    )
    from src.blm.ppt_charts import PPTChartGenerator
    PPT_AVAILABLE = True
except ImportError:
    PPT_AVAILABLE = False
    BLMPPTGenerator = None
    BLMPPTGeneratorEnhanced = None
    PPTChartGenerator = None
    generate_blm_ppt = None
    generate_enhanced_blm_ppt = None

# Optional Canva integration
from src.blm.canva_integration import (
    CanvaBLMExporter,
    check_canva_credentials,
)

__all__ = [
    # Data models
    "GLOBAL_OPERATORS",
    "BUSINESS_SEGMENTS",
    "COMPETITIVE_DIMENSIONS",
    "OperatorProfile",
    "MarketContext",
    "TelecomDataGenerator",
    "generate_sample_data",
    # Five Looks
    "InsightResult",
    "FiveLooksAnalyzer",
    # Three Decisions
    "StrategyItem",
    "StrategyResult",
    "ThreeDecisionsEngine",
    # Report generation
    "BLMReportGenerator",
    # PPT generation
    "BLMPPTGenerator",
    "BLMPPTGeneratorEnhanced",
    "PPTChartGenerator",
    "generate_blm_ppt",
    "generate_enhanced_blm_ppt",
    "PPT_AVAILABLE",
    # Canva integration
    "CanvaBLMExporter",
    "check_canva_credentials",
    # CLI
    "blm_cli",
    # Convenience functions
    "generate_blm_strategy",
]
