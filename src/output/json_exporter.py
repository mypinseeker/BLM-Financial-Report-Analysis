"""JSON exporter for BLM Five Looks analysis results.

Serializes FiveLooksResult to structured JSON with custom handling
for datetime, Enum, and ProvenanceStore objects.

Usage:
    exporter = BLMJsonExporter()
    path = exporter.export(result, "output/analysis.json")
"""

from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class _BLMEncoder(json.JSONEncoder):
    """Custom JSON encoder for BLM data models."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        return super().default(obj)


class BLMJsonExporter:
    """Export FiveLooksResult to JSON."""

    def export(
        self,
        result,
        output_path: Optional[str] = None,
        include_provenance: bool = True,
        indent: int = 2,
    ) -> str:
        """Export analysis result to JSON.

        Args:
            result: FiveLooksResult from the analysis engine
            output_path: File path to write JSON (returns string if None)
            include_provenance: Whether to include provenance data
            indent: JSON indentation level

        Returns:
            Path to written file, or JSON string if output_path is None
        """
        data = self._build_structure(result, include_provenance)
        json_str = json.dumps(data, cls=_BLMEncoder, indent=indent, ensure_ascii=False)

        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json_str, encoding='utf-8')
            return str(path)
        return json_str

    def _build_structure(self, result, include_provenance: bool) -> dict:
        """Build the top-level JSON structure."""
        structure = {
            "meta": {
                "target_operator": result.target_operator,
                "market": result.market,
                "analysis_period": result.analysis_period,
                "generated_at": datetime.now().isoformat(),
                "format_version": "1.0",
            },
            "five_looks": {
                "trends": self._serialize(result.trends),
                "market_customer": self._serialize(result.market_customer),
                "competition": self._serialize(result.competition),
                "self_analysis": self._serialize(result.self_analysis),
                "swot": self._serialize(result.swot),
                "opportunities": self._serialize(result.opportunities),
            },
        }

        if include_provenance and result.provenance:
            structure["data_quality"] = result.provenance.quality_report()
            structure["provenance"] = {
                "footnotes": result.provenance.to_footnotes(),
                "source_count": len(result.provenance._sources),
                "value_count": len(result.provenance._values),
            }

        return structure

    def _serialize(self, obj) -> Any:
        """Serialize a data model object."""
        if obj is None:
            return None
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return self._dataclass_to_dict(obj)
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, list):
            return [self._serialize(item) for item in obj]
        if isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return {k: self._serialize(v) for k, v in obj.__dict__.items()
                    if not k.startswith('_')}
        return str(obj)

    def _dataclass_to_dict(self, obj) -> dict:
        """Convert a dataclass to dict with custom serialization."""
        result = {}
        for f in dataclasses.fields(obj):
            value = getattr(obj, f.name)
            result[f.name] = self._serialize(value)
        return result
