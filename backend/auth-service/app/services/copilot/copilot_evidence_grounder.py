"""
TruthShield X — Copilot Evidence Grounder & Citation Engine (Phase 20).

Constructs evidence-grounded answer contracts with explicit citations, contradictions, and unknown handling.
"""

from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.copilot_command_models import (
    AnswerContractDTO,
    EvidenceCitationDTO,
    EpistemicStatusLiteral,
)


class CopilotEvidenceGrounder:
    """Ensures answers comply strictly with the TruthShield X Answer Contract."""

    def format_answer(
        self,
        answer: str,
        citations: Optional[List[EvidenceCitationDTO]] = None,
        confidence: float = 0.90,
        sources: Optional[List[str]] = None,
        contradictions: Optional[List[str]] = None,
        unknown_areas: Optional[List[str]] = None,
        limitations: Optional[List[str]] = None,
        epistemic_status: EpistemicStatusLiteral = "VERIFIED",
    ) -> AnswerContractDTO:
        return AnswerContractDTO(
            answer=answer,
            evidence=citations or [],
            confidence=confidence,
            sources=sources or ["TELEMETRY_ENGINE", "EVIDENCE_GRAPH"],
            contradictions=contradictions or [],
            unknown_areas=unknown_areas or [],
            limitations=limitations or ["Analysis bound to verified tenant telemetry."],
            epistemic_status=epistemic_status,
        )

    def create_citation(
        self,
        evidence_id: str,
        source_id: str,
        object_id: str,
        snippet: str,
        confidence: float = 0.95,
    ) -> EvidenceCitationDTO:
        return EvidenceCitationDTO(
            evidence_id=evidence_id,
            source_id=source_id,
            object_id=object_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            snippet=snippet,
            confidence=confidence,
        )
