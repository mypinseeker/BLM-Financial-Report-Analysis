"""Canva API Integration for BLM Reports.

Provides integration with Canva Connect API to create presentations
from BLM analysis results.

NOTE: Canva's Autofill API requires an Enterprise account.
For users without Enterprise access, use the python-pptx based
BLMPPTGenerator instead.

Setup:
1. Create a Canva Developer account: https://www.canva.com/developers/
2. Create an integration and get API credentials
3. Set environment variables:
   - CANVA_CLIENT_ID
   - CANVA_CLIENT_SECRET
   - CANVA_ACCESS_TOKEN (or use OAuth flow)

Usage:
    from src.blm.canva_integration import CanvaBLMExporter

    exporter = CanvaBLMExporter(access_token="your_token")
    design_url = exporter.create_presentation(five_looks, three_decisions, ...)
"""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

from src.blm.five_looks import InsightResult
from src.blm.three_decisions import StrategyResult


# =============================================================================
# Canva API Configuration
# =============================================================================

CANVA_API_BASE = "https://api.canva.com/rest/v1"

@dataclass
class CanvaConfig:
    """Canva API configuration."""
    client_id: str
    client_secret: str
    access_token: str
    api_base: str = CANVA_API_BASE


@dataclass
class CanvaSlideData:
    """Data structure for a single Canva slide."""
    slide_type: str  # "title", "section", "content", "metrics", "closing"
    title: str
    subtitle: str = ""
    content: list = None
    metrics: dict = None
    recommendations: list = None
    priority_items: list = None


class CanvaBLMExporter:
    """Export BLM analysis results to Canva presentations.

    Requires Canva Enterprise account for full functionality.
    """

    def __init__(
        self,
        access_token: str = None,
        client_id: str = None,
        client_secret: str = None,
    ):
        """Initialize Canva exporter.

        Args:
            access_token: Canva API access token (or set CANVA_ACCESS_TOKEN env var)
            client_id: Canva client ID (or set CANVA_CLIENT_ID env var)
            client_secret: Canva client secret (or set CANVA_CLIENT_SECRET env var)
        """
        self.access_token = access_token or os.getenv("CANVA_ACCESS_TOKEN")
        self.client_id = client_id or os.getenv("CANVA_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("CANVA_CLIENT_SECRET")

        if not self.access_token:
            raise ValueError(
                "Canva access token required. Set CANVA_ACCESS_TOKEN environment variable "
                "or pass access_token parameter. "
                "For users without Canva Enterprise, use BLMPPTGenerator instead."
            )

        self.api_base = CANVA_API_BASE

    def create_presentation(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str] = None,
        title: str = None,
        template_id: str = None,
    ) -> dict:
        """Create a Canva presentation from BLM analysis.

        Args:
            five_looks: Five Looks analysis results
            three_decisions: Three Decisions strategy results
            target_operator: Target operator name
            competitors: List of competitor names
            title: Presentation title
            template_id: Canva template ID (optional, uses default if not provided)

        Returns:
            Dict with design_id and edit_url
        """
        competitors = competitors or []
        title = title or f"{target_operator} BLM 战略分析报告"

        # Prepare slide data
        slides_data = self._prepare_slides_data(
            five_looks, three_decisions, target_operator, competitors, title
        )

        # Create design via Canva API
        design_data = self._create_design(title, template_id)

        # If using Autofill API (Enterprise), populate slides
        if template_id:
            self._autofill_design(design_data["design_id"], slides_data)

        return {
            "design_id": design_data.get("design_id"),
            "edit_url": design_data.get("urls", {}).get("edit_url"),
            "view_url": design_data.get("urls", {}).get("view_url"),
            "slides_data": slides_data,
        }

    def _prepare_slides_data(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str],
        title: str,
    ) -> list[CanvaSlideData]:
        """Prepare structured slide data for Canva."""
        slides = []

        # Title slide
        slides.append(CanvaSlideData(
            slide_type="title",
            title=title,
            subtitle=f"基于 BLM (Business Leadership Model) 方法论",
            content=[
                f"分析对象: {target_operator}",
                f"竞争对手: {', '.join(competitors)}" if competitors else "",
                f"报告日期: {datetime.now().strftime('%Y年%m月%d日')}",
            ],
        ))

        # Agenda slide
        slides.append(CanvaSlideData(
            slide_type="content",
            title="报告目录",
            subtitle="AGENDA",
            content=[
                "01 执行摘要 - Executive Summary",
                "02 五看分析 - Five Looks Analysis",
                "03 三定策略 - Three Decisions Strategy",
                "04 总结与建议 - Summary & Recommendations",
            ],
        ))

        # Executive Summary
        self_insight = five_looks.get("self")
        strategy = three_decisions.get("strategy")

        exec_metrics = {}
        if self_insight and self_insight.metrics:
            exec_metrics = {
                "收入规模": f"€{self_insight.metrics.get('revenue_eur_billion', 'N/A')}B",
                "市场排名": f"第{self_insight.metrics.get('revenue_rank', 'N/A')}位",
                "市场份额": f"{self_insight.metrics.get('market_share_pct', 'N/A')}%",
                "5G覆盖率": f"{self_insight.metrics.get('5g_coverage_pct', 'N/A')}%",
            }

        p0_strategies = []
        if strategy:
            p0_strategies = [
                {"priority": i.priority, "name": i.name, "description": i.description}
                for i in strategy.items if i.priority == "P0"
            ][:3]

        slides.append(CanvaSlideData(
            slide_type="metrics",
            title="执行摘要",
            subtitle="EXECUTIVE SUMMARY",
            metrics=exec_metrics,
            priority_items=p0_strategies,
        ))

        # Section divider - Five Looks
        slides.append(CanvaSlideData(
            slide_type="section",
            title="五看分析",
            subtitle="Five Looks Analysis",
        ))

        # Five Looks slides
        for key, insight in five_looks.items():
            slides.append(CanvaSlideData(
                slide_type="content",
                title=insight.title,
                subtitle=insight.category.upper(),
                metrics=insight.metrics,
                content=insight.findings[:6],
                recommendations=insight.recommendations[:4],
            ))

        # Section divider - Three Decisions
        slides.append(CanvaSlideData(
            slide_type="section",
            title="三定策略",
            subtitle="Three Decisions Strategy",
        ))

        # Three Decisions slides
        for key, decision in three_decisions.items():
            priority_items = [
                {"priority": i.priority, "name": i.name, "description": i.description, "kpis": i.kpis}
                for i in decision.items[:5]
            ]

            slides.append(CanvaSlideData(
                slide_type="content",
                title=decision.title,
                subtitle=decision.decision_type.upper(),
                content=decision.summary.split("\n")[:5],
                priority_items=priority_items,
            ))

        # Conclusion slide
        execution = three_decisions.get("execution")
        milestones = []
        if execution:
            milestones = [
                f"{i.timeline}: {i.name}"
                for i in execution.items
                if i.category == "milestone" and i.timeline
            ][:5]

        slides.append(CanvaSlideData(
            slide_type="content",
            title="总结与建议",
            subtitle="SUMMARY",
            priority_items=p0_strategies,
            content=milestones,
        ))

        # Closing slide
        slides.append(CanvaSlideData(
            slide_type="closing",
            title="谢谢",
            subtitle="THANK YOU",
        ))

        return slides

    def _create_design(self, title: str, template_id: str = None) -> dict:
        """Create a new Canva design via API.

        Args:
            title: Design title
            template_id: Optional template ID

        Returns:
            Design creation response
        """
        endpoint = f"{self.api_base}/designs"

        payload = {
            "design_type": "presentation",
            "title": title,
        }

        if template_id:
            payload["template_id"] = template_id

        return self._api_request("POST", endpoint, payload)

    def _autofill_design(self, design_id: str, slides_data: list[CanvaSlideData]) -> dict:
        """Autofill design with data (requires Enterprise).

        Args:
            design_id: Canva design ID
            slides_data: List of slide data

        Returns:
            Autofill response
        """
        endpoint = f"{self.api_base}/designs/{design_id}/autofill"

        # Convert slides data to Canva autofill format
        data_fields = {}
        for i, slide in enumerate(slides_data):
            prefix = f"slide_{i+1}"
            data_fields[f"{prefix}_title"] = slide.title
            data_fields[f"{prefix}_subtitle"] = slide.subtitle

            if slide.content:
                for j, content in enumerate(slide.content[:6]):
                    data_fields[f"{prefix}_content_{j+1}"] = content

            if slide.metrics:
                for key, value in slide.metrics.items():
                    safe_key = key.replace(" ", "_").lower()
                    data_fields[f"{prefix}_metric_{safe_key}"] = str(value)

        payload = {"data": data_fields}
        return self._api_request("POST", endpoint, payload)

    def _api_request(self, method: str, endpoint: str, payload: dict = None) -> dict:
        """Make API request to Canva.

        Args:
            method: HTTP method
            endpoint: API endpoint
            payload: Request payload

        Returns:
            API response as dict
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        data = json.dumps(payload).encode("utf-8") if payload else None

        request = urllib.request.Request(
            endpoint,
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise CanvaAPIError(
                f"Canva API error ({e.code}): {error_body}"
            ) from e
        except urllib.error.URLError as e:
            raise CanvaAPIError(f"Network error: {e.reason}") from e

    def export_slides_json(
        self,
        five_looks: dict[str, InsightResult],
        three_decisions: dict[str, StrategyResult],
        target_operator: str,
        competitors: list[str] = None,
        output_path: str = None,
    ) -> str:
        """Export slides data as JSON for manual Canva import.

        Useful when API access is not available - users can manually
        create the presentation in Canva using this data.

        Args:
            five_looks: Five Looks analysis results
            three_decisions: Three Decisions strategy results
            target_operator: Target operator name
            competitors: List of competitor names
            output_path: Output file path

        Returns:
            Path to exported JSON file
        """
        competitors = competitors or []
        title = f"{target_operator} BLM 战略分析报告"

        slides_data = self._prepare_slides_data(
            five_looks, three_decisions, target_operator, competitors, title
        )

        # Convert to JSON-serializable format
        export_data = {
            "title": title,
            "target_operator": target_operator,
            "competitors": competitors,
            "generated_at": datetime.now().isoformat(),
            "slides": [asdict(slide) for slide in slides_data],
            "instructions": {
                "en": "Use this data to manually create a presentation in Canva. "
                      "Each slide object contains the content for one slide.",
                "zh": "使用此数据在 Canva 中手动创建演示文稿。"
                      "每个 slide 对象包含一张幻灯片的内容。",
            },
        }

        if output_path is None:
            output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            safe_name = target_operator.lower().replace(" ", "_")
            output_path = str(output_dir / f"canva_slides_{safe_name}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        return output_path


class CanvaAPIError(Exception):
    """Canva API error."""
    pass


# =============================================================================
# Utility Functions
# =============================================================================

def check_canva_credentials() -> bool:
    """Check if Canva credentials are configured.

    Returns:
        True if credentials are available
    """
    return bool(os.getenv("CANVA_ACCESS_TOKEN"))


def get_canva_auth_url(client_id: str, redirect_uri: str, scopes: list = None) -> str:
    """Get Canva OAuth authorization URL.

    Args:
        client_id: Canva client ID
        redirect_uri: OAuth redirect URI
        scopes: List of required scopes

    Returns:
        Authorization URL
    """
    scopes = scopes or ["design:content:read", "design:content:write"]
    scope_str = " ".join(scopes)

    return (
        f"https://www.canva.com/api/oauth/authorize?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope_str}"
    )
