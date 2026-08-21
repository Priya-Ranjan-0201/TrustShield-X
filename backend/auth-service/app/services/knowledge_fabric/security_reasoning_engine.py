"""
TruthShield X — Security Reasoning Engine (Phase 19).

Synthesizes knowledge graph, evidence graph, temporal history, and telemetry into conclusions with explainable reasoning traces.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    ReasoningTraceDTO,
    EpistemicStatusLiteral,
)


class SecurityReasoningEngine:
    """Produces explainable conclusions with explicit evidence links, assumptions, and limitations."""

    def __init__(self):
        self._traces: Dict[str, ReasoningTraceDTO] = {}
        self._initialize_default_trace()

    def _initialize_default_trace(self):
        trace = ReasoningTraceDTO(
            conclusion_id="conc_01",
            conclusion_statement="Checkout API is critically vulnerable to external RCE from Shadow Hydra C2 servers.",
            supporting_evidence=["ev_pcap_trace_88", "ev_vuln_scan_44", "ev_threat_intel_feed"],
            relationships=["srv_checkout_production HOSTS svc_payment_gateway", "svc_payment_gateway EXPOSES cve_2026_9942"],
            assumptions=["WAF inspection rule for header manipulation is currently in monitor-only mode"],
            confidence=0.89,
            contradictions=["Kubernetes container audit shows rapid restart"],
            limitations=["Absence of full memory core dump on host"],
            epistemic_status="INFERENCE",
        )
        self._traces[trace.conclusion_id] = trace

    def generate_reasoning_trace(
        self,
        statement: str,
        supporting_evidence: List[str],
        relationships: List[str],
        assumptions: List[str],
        confidence: float = 0.85,
        contradictions: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
        epistemic_status: EpistemicStatusLiteral = "INFERENCE",
    ) -> ReasoningTraceDTO:
        trace = ReasoningTraceDTO(
            conclusion_statement=statement,
            supporting_evidence=supporting_evidence,
            relationships=relationships,
            assumptions=assumptions,
            confidence=confidence,
            contradictions=contradictions or [],
            limitations=limitations or [],
            epistemic_status=epistemic_status,
        )
        self._traces[trace.conclusion_id] = trace
        return trace

    def get_trace(self, conclusion_id: str) -> Optional[ReasoningTraceDTO]:
        return self._traces.get(conclusion_id)

    def list_traces(self) -> List[ReasoningTraceDTO]:
        return list(self._traces.values())
