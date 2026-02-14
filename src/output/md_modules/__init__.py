"""Module renderers for BLM Strategic Insight MD report.

Each module exports a `render_*()` function with signature:
    def render_module(result, diagnosis, config) -> str
"""
from .executive_summary import render_executive_summary
from .trends import render_trends
from .market_customer import render_market_customer
from .tariff import render_tariff
from .competition import render_competition
from .self_analysis import render_self_analysis
from .swot import render_swot
from .opportunities import render_opportunities
from .decisions import render_decisions

__all__ = [
    "render_executive_summary",
    "render_trends",
    "render_market_customer",
    "render_tariff",
    "render_competition",
    "render_self_analysis",
    "render_swot",
    "render_opportunities",
    "render_decisions",
]
