"""
TruthShield X — Temporal Threat Graph Engine (Phase 27).

Maintains a time-aware intelligence graph supporting historical and temporal queries.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


class TemporalThreatGraphEngine:
    """Provides time-aware graph traversals connecting indicators, campaigns, assets, and controls."""

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {
            "node_darkstorm_c2": {"type": "INFRASTRUCTURE", "first_seen": "2026-08-01T00:00:00Z", "status": "ACTIVE"},
            "node_ast_api_gw": {"type": "ASSET", "first_seen": "2026-01-01T00:00:00Z", "status": "ACTIVE"},
        }
        self._edges: List[Dict[str, Any]] = [
            {
                "source": "node_darkstorm_c2",
                "target": "node_ast_api_gw",
                "relation": "TARGETS",
                "valid_from": "2026-08-10T00:00:00Z",
                "valid_until": "2026-09-01T00:00:00Z",
                "confidence": 0.94,
            }
        ]

    def query_temporal_relationships(self, entity_id: str, query_time: Optional[str] = None) -> List[Dict[str, Any]]:
        target_time = query_time or datetime.now(timezone.utc).isoformat()
        results = []
        for edge in self._edges:
            if edge["source"] == entity_id or edge["target"] == entity_id:
                if edge["valid_from"] <= target_time <= edge.get("valid_until", target_time):
                    results.append(edge)
        return results
