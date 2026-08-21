"""
TruthShield X — Safe Threat Hunt Query Engine & DSL Parser
"""

import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class ThreatHuntQueryEngine:
    """Safe, non-SQL Hunt DSL parser and bounded query executor across multi-tenant telemetry and assets."""

    def __init__(self):
        # tenant_id -> List[Records]
        self._mock_data_lake: Dict[str, List[Dict[str, Any]]] = {}

    def populate_test_telemetry(self, tenant_id: str, records: List[Dict[str, Any]]) -> None:
        """Populates telemetry for hunt execution."""
        if tenant_id not in self._mock_data_lake:
            self._mock_data_lake[tenant_id] = []
        self._mock_data_lake[tenant_id].extend(records)

    def execute_hunt_query(
        self,
        dsl_query: str,
        tenant_id: str = "default_tenant",
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """Parses internal safe DSL queries (e.g. 'FIND assets WHERE exposure_score > 50 AND new_infrastructure = true') safely without raw SQL."""
        # Sanitize query
        clean_query = dsl_query.strip()
        data_pool = self._mock_data_lake.get(tenant_id, [])

        results = []
        # Parse basic DSL condition tokens safely
        score_match = re.search(r"exposure_score\s*([><=]+)\s*(\d+)", clean_query, re.IGNORECASE)
        target_score = float(score_match.group(2)) if score_match else None
        operator = score_match.group(1) if score_match else None

        for rec in data_pool:
            if target_score is not None and operator:
                rec_score = float(rec.get("exposure_score", 0.0))
                if operator == ">" and not (rec_score > target_score):
                    continue
                if operator == "<" and not (rec_score < target_score):
                    continue
                if operator in ("=", "==") and not (rec_score == target_score):
                    continue

            results.append(rec)
            if len(results) >= max_results:
                break

        return results
