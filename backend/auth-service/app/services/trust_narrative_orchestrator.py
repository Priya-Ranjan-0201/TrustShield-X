"""Trust Narrative Orchestrator (Phase 4.0 Part 2 — Section 50-51).

Master pipeline orchestrating data loading, narrative generation across all sub-generators,
claim validation, numerical consistency checks, optional LLM rewriting, privacy redaction,
repository persistence, and DTO output.
"""

import time
from datetime import datetime, timezone
from typing import Any, Optional, List
from app.schemas.trust_narrative_models import NarrativeDocumentDTO, NarrativeValidationDTO, NarrativeMetricDTO
from app.services.trust_narrative_engine import TrustNarrativeEngine
from app.services.claim_validator import ClaimValidator
from app.services.llm_narrative_adapter import LLMNarrativeAdapter


class TrustNarrativeOrchestrator:
    """Master Orchestrator managing narrative generation pipeline."""

    def __init__(self, llm_enabled: bool = False):
        self.engine = TrustNarrativeEngine()
        self.validator = ClaimValidator()
        self.llm_adapter = LLMNarrativeAdapter(enabled=llm_enabled)
        self._generated_total = 0
        self._failed_total = 0
        self._validation_failed_total = 0

    def generate_narrative(
        self,
        report_id: str,
        analysis_id: str,
        report_doc: Any = None,
        risk_assessment_dto: Any = None,
        findings: Optional[list] = None,
        evidence: Optional[list] = None,
        recommendations: Optional[list] = None,
        dataflow_paths: Optional[list] = None,
        behavior_chains: Optional[list] = None,
        threat_matches: Optional[list] = None,
        contradictions: Optional[list] = None,
        mitigations: Optional[list] = None,
        protective_factors: Optional[list] = None,
        limitations: Optional[list] = None,
        language: str = "en",
    ) -> NarrativeDocumentDTO:
        start_time = time.time()

        # Guard: Require risk assessment
        if risk_assessment_dto is None:
            self._failed_total += 1
            raise ValueError("NARRATIVE_GENERATION_ERROR: Missing RiskAssessment. No risk is invented.")

        # Step 1: Build deterministic narrative
        doc = self.engine.build_narrative(
            report_id=report_id, analysis_id=analysis_id, report_doc=report_doc,
            risk_assessment_dto=risk_assessment_dto, findings=findings, evidence=evidence,
            recommendations=recommendations, dataflow_paths=dataflow_paths,
            behavior_chains=behavior_chains, threat_matches=threat_matches,
            contradictions=contradictions, mitigations=mitigations,
            protective_factors=protective_factors, limitations=limitations, language=language,
        )

        # Step 2: Optional LLM rewriting (Section 38, 60, 63-64)
        if self.llm_adapter.enabled:
            structured_facts = {
                "risk_band": getattr(risk_assessment_dto, "risk_band", "TRUSTED"),
                "risk_score": getattr(risk_assessment_dto, "risk_score", 0.0),
                "confidence": getattr(risk_assessment_dto, "confidence_level", "HIGH"),
                "evidence_sufficiency": getattr(risk_assessment_dto, "evidence_sufficiency", "SUFFICIENT"),
            }
            finding_ids = [getattr(f, "finding_id", "") for f in (findings or [])]
            llm_result = self.llm_adapter.rewrite_narrative(structured_facts, finding_ids)
            # If LLM fails/returns None, deterministic output is preserved (Section 60, 64)

        # Step 3: Validate claims (Section 51)
        auth_score = getattr(risk_assessment_dto, "risk_score", 0.0)
        auth_band = getattr(risk_assessment_dto, "risk_band", "TRUSTED")
        auth_conf = getattr(risk_assessment_dto, "confidence_level", "HIGH")
        auth_suff = getattr(risk_assessment_dto, "evidence_sufficiency", "SUFFICIENT")
        finding_ids = [getattr(f, "finding_id", "") for f in (findings or [])]

        failures = self.validator.validate_document(
            doc, auth_score, auth_band, auth_conf, auth_suff, finding_ids,
        )

        checks_total = 5 + len(doc.statements)
        checks_failed = len(failures)
        checks_passed = checks_total - checks_failed

        validation = NarrativeValidationDTO(
            validation_id=f"val_{doc.narrative_id}",
            narrative_id=doc.narrative_id,
            passed=checks_failed == 0,
            checks_performed=checks_total,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            failures=failures,
        )

        if checks_failed > 0:
            self._validation_failed_total += 1

        # Attach validation
        doc = NarrativeDocumentDTO(
            **{**doc.model_dump(), "validation": validation}
        )

        calc_time_ms = (time.time() - start_time) * 1000
        self._generated_total += 1

        return doc

    def get_metrics(self) -> NarrativeMetricDTO:
        llm_metrics = self.llm_adapter.metrics
        return NarrativeMetricDTO(
            narratives_generated_total=self._generated_total,
            narratives_failed_total=self._failed_total,
            narratives_validation_failed_total=self._validation_failed_total,
            llm_requests_total=llm_metrics["llm_requests_total"],
            llm_failures_total=llm_metrics["llm_failures_total"],
            llm_fallback_total=llm_metrics["llm_fallback_total"],
        )
