"""
TruthShield X — Copilot Request Classifier (Phase 20).

Classifies user requests into standardized security intents.
"""

from typing import Dict, Any
from app.schemas.copilot_command_models import RequestClassificationLiteral


class CopilotRequestClassifier:
    """Classifies user prompts into security workflows."""

    def classify_request(self, prompt: str) -> RequestClassificationLiteral:
        p_lower = prompt.lower().strip()

        if not p_lower:
            return "ASK_CLARIFICATION"

        if any(w in p_lower for w in ["block", "isolate", "quarantine", "revoke", "disable", "remediate", "execute"]):
            return "ACTION_REQUEST"
        if any(w in p_lower for w in ["simulate", "what if", "dry run", "predict outcome"]):
            return "SIMULATION"
        if any(w in p_lower for w in ["hunt", "query", "search logs", "ioc match"]):
            return "HUNT"
        if any(w in p_lower for w in ["investigate", "timeline", "who did", "attack path"]):
            return "INVESTIGATION"
        if any(w in p_lower for w in ["posture", "executive", "board", "ciso", "leadership", "risk summary"]):
            return "EXECUTIVE_QUERY"
        if any(w in p_lower for w in ["report", "generate brief", "post-incident", "summary document"]):
            return "REPORTING"
        if any(w in p_lower for w in ["policy", "compliance", "pci-dss", "exception", "audit requirement"]):
            return "GOVERNANCE"
        if any(w in p_lower for w in ["incident", "alert triage", "containment plan", "response options"]):
            return "INCIDENT_RESPONSE"
        if any(w in p_lower for w in ["why", "analyze", "root cause", "explain risk", "correlate"]):
            return "ANALYSIS"
        if any(w in p_lower for w in ["what should", "recommend", "next step"]):
            return "RECOMMENDATION"

        return "INFORMATION"
