"""
TruthShield X — Prompt Security Engine (Phase 31).

Detects direct prompt injection attempts, manages immutable prompt templates, and runs adversarial regression tests.
"""

from typing import Dict, List, Optional, Any
from app.schemas.ai_security_governance_models import PromptTemplateDTO


class PromptSecurityEngine:
    """Guards system prompts and detects adversarial jailbreak/injection attacks in real-time."""

    def __init__(self):
        self._prompts: Dict[str, PromptTemplateDTO] = {}
        self._seed_default_prompt()

    def _seed_default_prompt(self):
        p1 = PromptTemplateDTO(
            prompt_id="pmt_incident_triage_v1",
            name="Incident Triage & Grounded Recommendation Prompt",
            version="1.2.0",
            owner="SOC_AUTOMATION_LEAD",
            purpose="Synthesizes early warnings and recommends containment with strict evidence citations",
            system_instructions="You are TruthShield X Security Copilot. Ground all claims in provided evidence.",
            allowed_tools=["query_threat_graph", "fetch_control_status"],
            security_constraints=["NEVER_REVEAL_SYSTEM_PROMPT", "NEVER_BYPASS_RBAC"],
            status="APPROVED",
        )
        self._prompts[p1.prompt_id] = p1

    def inspect_prompt_input(self, user_input: str) -> Dict[str, Any]:
        lower_input = user_input.lower()
        injection_patterns = [
            "ignore instructions",
            "ignore previous instructions",
            "ignore all previous instructions",
            "reveal system prompt",
            "reveal the system prompt",
            "give me the database credentials",
            "execute this command",
            "disable tenant isolation",
            "bypass authorization",
            "drop table",
        ]

        for p in injection_patterns:
            if p in lower_input:
                return {
                    "is_safe": False,
                    "status": "PROMPT_INJECTION_DETECTED",
                    "matched_pattern": p,
                    "sanitized_response": "Request blocked: Prompt injection attempt detected.",
                }

        return {
            "is_safe": True,
            "status": "CLEAN",
            "matched_pattern": None,
            "sanitized_response": user_input,
        }

    def list_prompts(self) -> List[PromptTemplateDTO]:
        return list(self._prompts.values())
