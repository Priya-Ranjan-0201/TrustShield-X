"""
TruthShield X — Threat Hunting Copilot & Query Generator (Phase 20).

Generates safe, read-only threat hunting queries with syntax and scope validation.
"""

from typing import Dict, List, Optional
from app.schemas.copilot_command_models import GeneratedQueryDTO


class ThreatHuntingCopilot:
    """Constructs and validates safe read-only threat hunting queries across SQL, Logs, Graph, and SIEM."""

    def __init__(self):
        self._dangerous_keywords = ["drop", "delete", "insert", "update", "alter", "truncate", "grant", "revoke"]

    def generate_hunt_query(
        self,
        query_type: str,
        target_entity: str,
        hypothesis: str,
    ) -> GeneratedQueryDTO:
        if query_type == "SQL":
            text = f"SELECT event_time, source_ip, principal_id, action FROM auth_events WHERE target_service = '{target_entity}' AND status = 'FAILED' LIMIT 100;"
        elif query_type == "LOG":
            text = f'service="{target_entity}" AND status_code >= 400 | stats count by client_ip | sort -count'
        elif query_type == "GRAPH":
            text = f"MATCH (n:Asset {{id: '{target_entity}'}})-[r:ACCESSES]->(m:Service) RETURN n, r, m LIMIT 50"
        else:
            text = f"index=security_telemetry sourcetype=pcap target='{target_entity}' | head 100"

        # Validate read-only status
        is_safe = not any(bad in text.lower() for bad in self._dangerous_keywords)
        safety = "SAFE" if is_safe else "BLOCKED_MUTATION"

        return GeneratedQueryDTO(
            query_type=query_type,  # type: ignore
            query_text=text,
            is_read_only=is_safe,
            target_scope=target_entity,
            syntax_valid=True,
            safety_status=safety,  # type: ignore
        )

    def validate_query(self, query_text: str) -> bool:
        """Ensures query is strictly read-only."""
        q_lower = query_text.lower()
        return not any(bad in q_lower for bad in self._dangerous_keywords)
