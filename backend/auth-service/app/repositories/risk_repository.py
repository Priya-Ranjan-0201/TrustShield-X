"""Repository for Risk Aggregation Database Operations (Phase 3.9 Part 1B).

Provides single-transaction bulk persistence and asynchronous CRUD queries across all 13 risk tables.
"""

import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.risk_aggregation import (
    RiskAssessmentModel,
    RiskFactorModel,
    RiskCategoryScoreModel,
    RiskContributionModel,
    RiskInteractionModel,
    RiskMitigationModel,
    RiskProtectiveFactorModel,
    RiskContradictionModel,
    RiskAuditRecordModel,
    RiskPolicyVersionModel,
    RiskDecisionRecordModel,
    RiskMetricModel,
)
from app.schemas.risk_aggregation_models import RiskAssessmentResultDTO


class RiskRepository:
    """Async SQLAlchemy repository for Risk Aggregation persistence and retrieval."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_risk_assessment(
        self, scan_id: uuid.UUID, dto: RiskAssessmentResultDTO
    ) -> RiskAssessmentModel:
        ass = dto.assessment
        assessment_model = RiskAssessmentModel(
            scan_id=scan_id,
            assessment_id=ass.assessment_id,
            risk_score=ass.risk_score,
            risk_band=ass.risk_band,
            confidence_level=ass.confidence_level,
            evidence_sufficiency=ass.evidence_sufficiency,
            decision_state=ass.decision_state,
            primary_risk_category=ass.primary_risk_category,
            risk_factor_count=ass.risk_factor_count,
            supporting_finding_count=ass.supporting_finding_count,
            contradictory_finding_count=ass.contradictory_finding_count,
            mitigating_factor_count=ass.mitigating_factor_count,
            protective_factor_count=ass.protective_factor_count,
            uncertainty_count=ass.uncertainty_count,
            engine_version=ass.engine_version,
            configuration_version=ass.configuration_version,
        )
        self.db.add(assessment_model)

        for f in dto.factors:
            self.db.add(
                RiskFactorModel(
                    scan_id=scan_id,
                    factor_id=f.factor_id,
                    category=f.category,
                    name=f.name,
                    description=f.description,
                    base_contribution=f.base_contribution,
                    final_contribution=f.final_contribution,
                    confidence=f.confidence,
                    evidence_sufficiency=f.evidence_sufficiency,
                    reason=f.reason,
                )
            )

        for cs in dto.category_scores:
            self.db.add(
                RiskCategoryScoreModel(
                    scan_id=scan_id,
                    category=cs.category,
                    raw_score=cs.raw_score,
                    normalized_score=cs.normalized_score,
                    risk_band=cs.risk_band,
                )
            )

        for c in dto.contributions:
            self.db.add(
                RiskContributionModel(
                    scan_id=scan_id,
                    finding_id=c.finding_id,
                    category=c.category,
                    contribution_weight=c.contribution_weight,
                )
            )

        for intr in dto.interactions:
            self.db.add(
                RiskInteractionModel(
                    scan_id=scan_id,
                    interaction_id=intr.interaction_id,
                    factor_a_id=intr.factor_a_id,
                    factor_b_id=intr.factor_b_id,
                    amplification_bonus=intr.amplification_bonus,
                    description=intr.description,
                )
            )

        for mit in dto.mitigations:
            self.db.add(
                RiskMitigationModel(
                    scan_id=scan_id,
                    mitigation_id=mit.mitigation_id,
                    description=mit.description,
                    reduction_amount=mit.reduction_amount,
                )
            )

        for prot in dto.protective_factors:
            self.db.add(
                RiskProtectiveFactorModel(
                    scan_id=scan_id,
                    protective_id=prot.protective_id,
                    description=prot.description,
                    reduction_amount=prot.reduction_amount,
                )
            )

        for cntr in dto.contradictions:
            self.db.add(
                RiskContradictionModel(
                    scan_id=scan_id,
                    contradiction_id=cntr.contradiction_id,
                    description=cntr.description,
                    uncertainty_penalty=cntr.uncertainty_penalty,
                )
            )

        aud = dto.audit_record
        self.db.add(
            RiskAuditRecordModel(
                scan_id=scan_id,
                audit_id=aud.audit_id,
                policy_version=aud.policy_version,
                configuration_checksum=aud.configuration_checksum,
                audit_trail_text=aud.audit_trail_text,
            )
        )

        dec = dto.decision_record
        self.db.add(
            RiskDecisionRecordModel(
                scan_id=scan_id,
                decision_id=dec.decision_id,
                decision_state=dec.decision_state,
                recommendation=dec.recommendation,
            )
        )

        m = dto.metrics
        self.db.add(
            RiskMetricModel(
                scan_id=scan_id,
                assessments_evaluated=m.assessments_evaluated,
                high_risk_assessments=m.high_risk_assessments,
                critical_risk_assessments=m.critical_risk_assessments,
                insufficient_evidence_assessments=m.insufficient_evidence_assessments,
            )
        )

        await self.db.commit()
        return assessment_model

    async def get_assessment_by_scan_id(self, scan_id: uuid.UUID) -> Optional[RiskAssessmentModel]:
        res = await self.db.execute(
            select(RiskAssessmentModel).where(RiskAssessmentModel.scan_id == scan_id)
        )
        scalars = res.scalars()
        if hasattr(scalars, "first"):
            item = scalars.first()
            if hasattr(item, "__await__"):
                item = await item
            return item
        return None
