"""Operator brand style library for PPT generation.

Defines color schemes, fonts, and sizing for each operator's brand identity.
Extended from the legacy PPTStyle with additional fields for the new output layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PPTStyle:
    """PPT style configuration for operator branding."""

    name: str
    display_name: str

    # Core colors (RGB tuples)
    primary_color: tuple  # Brand primary
    secondary_color: tuple  # Brand secondary
    accent_color: tuple  # Highlights
    text_color: tuple  # Body text
    light_text_color: tuple  # Secondary text / captions
    background_color: tuple  # Slide background

    # Semantic colors
    positive_color: tuple = (0, 128, 0)  # Green for positive metrics
    negative_color: tuple = (200, 0, 0)  # Red for negative metrics
    warning_color: tuple = (255, 165, 0)  # Orange for warnings
    neutral_color: tuple = (128, 128, 128)  # Gray for neutral

    # Fonts
    title_font: str = "Arial"
    body_font: str = "Arial"
    cjk_font: str = "Microsoft YaHei"  # For CJK characters

    # Font sizes (in Pt)
    title_size: int = 36
    subtitle_size: int = 24
    heading_size: int = 20
    body_size: int = 14
    small_size: int = 11
    footnote_size: int = 9

    # Key message bar
    key_message_bg: Optional[tuple] = None  # Defaults to primary_color
    key_message_text: tuple = (255, 255, 255)  # White text on bar

    # Chart palette (list of RGB tuples for multi-series charts)
    chart_palette: tuple = ()

    def __post_init__(self):
        if self.key_message_bg is None:
            self.key_message_bg = self.primary_color
        if not self.chart_palette:
            self.chart_palette = (
                self.primary_color,
                self.secondary_color,
                self.accent_color,
                (70, 130, 180),   # Steel blue
                (255, 165, 0),    # Orange
                (34, 139, 34),    # Forest green
            )


# --- Pre-defined operator styles ---

VODAFONE_STYLE = PPTStyle(
    name="vodafone",
    display_name="Vodafone",
    primary_color=(230, 0, 0),        # Vodafone Red #E60000
    secondary_color=(51, 51, 51),     # Dark Gray
    accent_color=(153, 0, 0),         # Dark Red
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    chart_palette=(
        (230, 0, 0),     # Vodafone Red
        (51, 51, 51),    # Dark Gray
        (153, 0, 0),     # Dark Red
        (70, 130, 180),  # Steel Blue
        (255, 165, 0),   # Orange
        (34, 139, 34),   # Green
    ),
)

DT_STYLE = PPTStyle(
    name="deutsche_telekom",
    display_name="Deutsche Telekom",
    primary_color=(226, 0, 116),      # Telekom Magenta #E20074
    secondary_color=(51, 51, 51),
    accent_color=(163, 0, 84),        # Dark Magenta
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    chart_palette=(
        (226, 0, 116),   # Magenta
        (51, 51, 51),    # Dark Gray
        (163, 0, 84),    # Dark Magenta
        (70, 130, 180),  # Steel Blue
        (255, 165, 0),   # Orange
        (34, 139, 34),   # Green
    ),
)

O2_STYLE = PPTStyle(
    name="telefonica_o2",
    display_name="Telefonica O2",
    primary_color=(0, 101, 163),      # O2 Blue #0065A3
    secondary_color=(51, 51, 51),
    accent_color=(0, 150, 214),       # Light Blue
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    chart_palette=(
        (0, 101, 163),   # O2 Blue
        (51, 51, 51),    # Dark Gray
        (0, 150, 214),   # Light Blue
        (255, 165, 0),   # Orange
        (34, 139, 34),   # Green
        (153, 0, 0),     # Dark Red
    ),
)

ONEANDONE_STYLE = PPTStyle(
    name="one_and_one",
    display_name="1&1",
    primary_color=(0, 55, 107),       # 1&1 Blue #00376B
    secondary_color=(51, 51, 51),
    accent_color=(0, 119, 200),       # Lighter Blue
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    chart_palette=(
        (0, 55, 107),    # 1&1 Blue
        (51, 51, 51),    # Dark Gray
        (0, 119, 200),   # Lighter Blue
        (255, 165, 0),   # Orange
        (34, 139, 34),   # Green
        (153, 0, 0),     # Dark Red
    ),
)

HUAWEI_STYLE = PPTStyle(
    name="huawei",
    display_name="Huawei",
    primary_color=(199, 0, 11),       # Huawei Red #C7000B
    secondary_color=(0, 0, 0),
    accent_color=(229, 32, 50),       # Lighter Red #E52032
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
    chart_palette=(
        (199, 0, 11),    # Huawei Red
        (0, 0, 0),       # Black
        (229, 32, 50),   # Lighter Red
        (70, 130, 180),  # Steel Blue
        (255, 165, 0),   # Orange
        (34, 139, 34),   # Green
    ),
)

DEFAULT_STYLE = PPTStyle(
    name="default",
    display_name="Default",
    primary_color=(0, 51, 102),       # Navy
    secondary_color=(51, 51, 51),
    accent_color=(70, 130, 180),      # Steel Blue
    text_color=(51, 51, 51),
    light_text_color=(128, 128, 128),
    background_color=(255, 255, 255),
)

# Style registry
STYLES = {
    "vodafone": VODAFONE_STYLE,
    "deutsche_telekom": DT_STYLE,
    "telefonica_o2": O2_STYLE,
    "one_and_one": ONEANDONE_STYLE,
    "huawei": HUAWEI_STYLE,
    "default": DEFAULT_STYLE,
}


# Operator brand colors for multi-operator charts
# Maps common name variants -> RGB tuple
OPERATOR_BRAND_COLORS: dict[str, tuple] = {
    # Deutsche Telekom — Magenta
    "DT": (226, 0, 116),
    "Deutsche Telekom": (226, 0, 116),
    "Telekom": (226, 0, 116),
    # Vodafone — Red
    "Vodafone": (230, 0, 0),
    "VF": (230, 0, 0),
    "Vodafone Germany": (230, 0, 0),
    # Telefonica O2 — Blue
    "O2": (0, 101, 163),
    "Telefonica O2": (0, 101, 163),
    "Telefonica": (0, 101, 163),
    # 1&1 — Dark Blue
    "1&1": (0, 55, 107),
    "1&1 AG": (0, 55, 107),
    # Combined label
    "O2/1&1": (0, 128, 128),
}


def get_style(operator_id: str) -> PPTStyle:
    """Get the PPT style for an operator, falling back to default."""
    return STYLES.get(operator_id, DEFAULT_STYLE)
