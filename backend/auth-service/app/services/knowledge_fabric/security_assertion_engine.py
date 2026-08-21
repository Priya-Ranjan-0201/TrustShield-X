"""
TruthShield X — Security Assertion Engine (Phase 19).

Constructs and verifies security assertions with explicit evidence trails and validation states.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    SecurityAssertionDTO,
    AssertionValidationStatusLiteral,
)


class SecurityAssertionEngine:
    """Manages verifiable security assertions, supporting/contradicting evidence links, and lifecycle validation."""

    def __init__(self):
        self._assertions: Dict[str, SecurityAssertionDTO] = {}
        self._initialize_default_assertions()

    def _initialize_default_assertions(self):
        asrt = SecurityAssertionDTO(
            assertion_id="asrt_checkout_at_risk",
            statement="Production Checkout Service is exposed to Shadow Hydra campaign via unpatched CVE-2026-9942.",
            supporting_evidence=["ev_pcap_trace_88", "ev_vuln_scan_44", "ev_threat_intel_feed"],
            contradicting_evidence=["ev_audit_log_90"],
            confidence=0.88,
            status="STRONGLY_SUPPORTED",
            provenance={"source": "SecurityReasoningEngine", "rule_id": "RULE_CAMPAIGN_VULN_EXPOSURE"},
        )
        self._assertions[asrt.assertion_id] = asrt

    def create_assertion(
        self,
        statement: str,
        supporting_evidence: Optional[List[str]] = None,
        contradicting_evidence: Optional[List[str]] = None,
        confidence: float = 0.85,
        status: AssertionValidationStatusLiteral = "SUPPORTED",
    ) -> SecurityAssertionDTO:
        """Registers a new assertion."""
        asrt = SecurityAssertionDTO(
            statement=statement,
            supporting_evidence=supporting_evidence or [],
            contradicting_evidence=contradicting_evidence or [],
            confidence=confidence,
            status=status,
        )
        self._assertions[asrt.assertion_id] = asrt
        return asrt

    def get_assertion(self, assertion_id: str) -> Optional[SecurityAssertionDTO]:
        return self._assertions.get(assertion_id)

    def list_assertions(self) -> List[SecurityAssertionDTO]:
        return list(self._assertions.values())
