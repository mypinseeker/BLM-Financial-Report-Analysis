"""Output generation layer for BLM analysis reports.

Supports PPT, HTML, JSON, TXT, and MD output formats.
PPT-related imports (ppt_charts, ppt_generator) are lazy-loaded
because they depend on numpy/matplotlib which may not be installed
in slim deployments (e.g. Vercel Lambda).
"""

from .ppt_styles import PPTStyle, get_style
from .json_exporter import BLMJsonExporter
from .txt_formatter import BLMTxtFormatter
from .html_generator import BLMHtmlGenerator
from .md_generator import BLMMdGenerator


def __getattr__(name):
    if name == "BLMChartGenerator":
        from .ppt_charts import BLMChartGenerator
        return BLMChartGenerator
    if name == "BLMPPTGenerator":
        from .ppt_generator import BLMPPTGenerator
        return BLMPPTGenerator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
