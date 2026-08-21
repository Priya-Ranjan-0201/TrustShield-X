"""Async Behavior Rule Repository Layer (Phase 3.9 Part 1A.24).

Provides database operations for persisting and retrieving behavior_rules, behavior_rule_versions,
behavior_rule_packs, behavior_rule_dependencies, behavior_rule_conditions, behavior_rule_evaluations,
behavior_rule_condition_results, behavior_rule_execution_traces, behavior_rule_evidence,
behavior_rule_suppressions, behavior_rule_exceptions, behavior_rule_conflicts, behavior_rule_metrics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.behavior_rule_engine import (
    BehaviorRuleModel,
    BehaviorRuleVersionModel,
    BehaviorRulePackModel,
    BehaviorRuleDependencyModel,
    BehaviorRuleConditionModel,
    BehaviorRuleEvaluationModel,
    BehaviorRuleConditionResultModel,
    BehaviorRuleExecutionTraceModel,
    BehaviorRuleEvidenceModel,
    BehaviorRuleSuppressionModel,
    BehaviorRuleExceptionModel,
    BehaviorRuleConflictModel,
    BehaviorRuleMetricModel,
)
from app.schemas.behavior_rule_models import RuleResultDTO


class BehaviorRuleRepository:
    """Async repository for Behavior Rule Engine DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_rule_result(
        self,
        scan_id: uuid.UUID,
        dto: RuleResultDTO,
    ) -> BehaviorRuleEvaluationModel:
        """Saves all 13 rule engine datasets inside one atomic transaction."""
        first_model = None

        for r in dto.rules:
            self.db.add(
                BehaviorRuleModel(
                    scan_id=scan_id,
                    rule_id=r.rule_id,
                    rule_version=r.rule_version,
                    namespace=r.namespace,
                    name=r.name,
                    description=r.description,
                    status=r.status,
                    severity_hint=r.severity_hint,
                    confidence_hint=r.confidence_hint,
                )
            )

        for p in dto.packs:
            self.db.add(
                BehaviorRulePackModel(
                    scan_id=scan_id,
                    pack_id=p.pack_id,
                    pack_version=p.pack_version,
                    rules_count=p.rules_count,
                    checksum=p.checksum,
                )
            )

        for e in dto.evaluations:
            m = BehaviorRuleEvaluationModel(
                scan_id=scan_id,
                evaluation_id=e.evaluation_id,
                rule_id=e.rule_id,
                rule_version=e.rule_version,
                namespace=e.namespace,
                state=e.state,
                confidence=e.confidence,
                evidence_provenance=e.evidence_provenance,
            )
            self.db.add(m)
            if not first_model:
                first_model = m

        for t in dto.traces:
            self.db.add(
                BehaviorRuleExecutionTraceModel(
                    scan_id=scan_id,
                    trace_id=t.trace_id,
                    rule_id=t.rule_id,
                    rule_version=t.rule_version,
                    duration_ms=t.duration_ms,
                    final_state=t.final_state,
                    confidence=t.confidence,
                )
            )

        for ev in dto.evidence:
            self.db.add(
                BehaviorRuleEvidenceModel(
                    scan_id=scan_id,
                    evidence_id=ev.evidence_id,
                    rule_id=ev.rule_id,
                    evidence_type=ev.evidence_type,
                    source_module=ev.source_module,
                )
            )

        for s in dto.suppressions:
            self.db.add(
                BehaviorRuleSuppressionModel(
                    scan_id=scan_id,
                    suppression_id=s.suppression_id,
                    rule_id=s.rule_id,
                    reason=s.reason,
                )
            )

        for ex in dto.exceptions:
            self.db.add(
                BehaviorRuleExceptionModel(
                    scan_id=scan_id,
                    exception_id=ex.exception_id,
                    rule_id=ex.rule_id,
                    scope=ex.scope,
                )
            )

        for c in dto.conflicts:
            self.db.add(
                BehaviorRuleConflictModel(
                    scan_id=scan_id,
                    conflict_id=c.conflict_id,
                    rule_a_id=c.rule_a_id,
                    rule_b_id=c.rule_b_id,
                    reason=c.reason,
                )
            )

        self.db.add(
            BehaviorRuleMetricModel(
                scan_id=scan_id,
                rules_loaded=dto.metrics.rules_loaded,
                rules_evaluated=dto.metrics.rules_evaluated,
                rules_matched=dto.metrics.rules_matched,
                rules_partially_matched=dto.metrics.rules_partially_matched,
                rules_not_evaluable=dto.metrics.rules_not_evaluable,
                rules_suppressed=dto.metrics.rules_suppressed,
                rules_conflicted=dto.metrics.rules_conflicted,
            )
        )

        if not first_model:
            first_model = BehaviorRuleEvaluationModel(
                scan_id=scan_id,
                evaluation_id="eval_default",
                rule_id="RULE-DEFAULT",
                rule_version="1.0.0",
                namespace="DATAFLOW",
                state="NOT_EVALUABLE",
                confidence="LOW",
                evidence_provenance="Default Record",
            )
            self.db.add(first_model)

        await self.db.commit()
        return first_model

    async def get_rule_evaluations(self, scan_id: uuid.UUID) -> List[BehaviorRuleEvaluationModel]:
        stmt = select(BehaviorRuleEvaluationModel).where(BehaviorRuleEvaluationModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
