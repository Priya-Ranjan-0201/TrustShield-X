"""Risk Aggregation Orchestrator (Phase 3.9 Part 1B).

Orchestrates loading canonical findings from Phase 3.9 Part 1A.25, executing risk aggregation,
generating audit records, explanations, multi-format exports, and persistence.
"""

import csv
import io
import json
import time
from typing import List, Dict, Any, Optional
from app.schemas.risk_aggregation_models import (
    RiskAssessmentDTO,
    RiskFactorDTO,
    RiskCategoryScoreDTO,
    RiskContributionDTO,
    RiskInteractionDTO,
    RiskMitigationDTO,
    RiskProtectiveFactorDTO,
    RiskContradictionDTO,
    RiskAuditRecordDTO,
    RiskPolicyVersionDTO,
    RiskDecisionRecordDTO,
    RiskMetricsDTO,
    RiskExplanationDTO,
    RiskSummaryDTO,
    RiskCardDTO,
    RiskAssessmentResultDTO,
)
from app.services.risk_aggregation_engine import RiskAggregationEngine


class RiskAggregationOrchestrator:
    """Orchestrates Risk Aggregation pipeline."""

    def __init__(self):
        self.engine = RiskAggregationEngine()

    def run_risk_assessment(
        self,
        consolidation_result_dto: Any = None,
    ) -> RiskAssessmentResultDTO:
        start_time = time.time()

        findings = getattr(consolidation_result_dto, "findings", []) if consolidation_result_dto else []

        (
            assessment,
            factors,
            category_scores,
            contributions,
            interactions,
            mitigations,
            protective_factors,
            contradictions,
        ) = self.engine.calculate_risk(canonical_findings=findings)

        audit_record = RiskAuditRecordDTO(
            audit_id=f"audit_{assessment.assessment_id}",
            policy_version="1.0.0",
            audit_trail_text=f"Evaluated {len(findings)} canonical findings into final risk score {assessment.risk_score:.2f} ({assessment.risk_band}).",
        )

        policy_ver = RiskPolicyVersionDTO()
        decision_rec = RiskDecisionRecordDTO(
            decision_id=f"dec_{assessment.assessment_id}",
            decision_state=assessment.decision_state,
        )

        metrics = RiskMetricsDTO(
            assessments_evaluated=1,
            high_risk_assessments=1 if assessment.risk_band == "HIGH_RISK" else 0,
            critical_risk_assessments=1 if assessment.risk_band == "CRITICAL_RISK" else 0,
        )

        explanation = RiskExplanationDTO(
            explanation_id=f"exp_{assessment.assessment_id}",
            summary_text=f"Final Cybersecurity Risk Assessment Score: {assessment.risk_score:.1f}/100 ({assessment.risk_band}). Evidence Sufficiency: {assessment.evidence_sufficiency}.",
            primary_reasons=[f.reason for f in factors[:5]],
        )

        summary = RiskSummaryDTO(
            title="Final Cybersecurity Risk Assessment Summary",
            risk_score=assessment.risk_score,
            risk_band=assessment.risk_band,
            confidence_level=assessment.confidence_level,
        )

        cards = [
            RiskCardDTO(
                card_id=f"card_{cs.category}",
                category=cs.category,
                score=cs.normalized_score,
                risk_band=cs.risk_band,
            )
            for cs in category_scores
        ]

        # Exporters
        json_exp = json.dumps(assessment.model_dump(), indent=2)

        csv_buf = io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(["Assessment ID", "Risk Score", "Risk Band", "Confidence", "Evidence Sufficiency", "Decision State"])
        writer.writerow([assessment.assessment_id, assessment.risk_score, assessment.risk_band, assessment.confidence_level, assessment.evidence_sufficiency, assessment.decision_state])
        csv_exp = csv_buf.getvalue()

        dot_exp = f'digraph RiskAssessment {{\n  "Assessment" [label="Score: {assessment.risk_score:.1f} ({assessment.risk_band})"];\n}}'
        mermaid_exp = f'graph TD\n  Assessment["Score: {assessment.risk_score:.1f} ({assessment.risk_band})"]'
        graphml_exp = '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n  <graph id="G" edgedefault="directed">\n    <node id="Assessment"/>\n  </graph>\n</graphml>'

        calc_time_ms = int((time.time() - start_time) * 1000)

        return RiskAssessmentResultDTO(
            assessment=assessment,
            factors=factors[:500],
            category_scores=category_scores[:500],
            contributions=contributions[:500],
            interactions=interactions[:500],
            mitigations=mitigations[:100],
            protective_factors=protective_factors[:100],
            contradictions=contradictions[:100],
            audit_record=audit_record,
            policy_version=policy_ver,
            decision_record=decision_rec,
            metrics=metrics,
            explanation=explanation,
            summary=summary,
            cards=cards[:100],
            json_export=json_exp,
            csv_export=csv_exp,
            graphml_export=graphml_exp,
            dot_export=dot_exp,
            mermaid_export=mermaid_exp,
            calculation_time_ms=calc_time_ms,
        )
