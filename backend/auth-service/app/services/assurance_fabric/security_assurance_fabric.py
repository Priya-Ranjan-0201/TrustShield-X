"""
TruthShield X — Continuous Security Assurance Fabric (Phase 24 Master Coordinator).

Orchestrates the complete 16-stage continuous security assurance lifecycle:
DISCOVER -> INVENTORY -> MAP CONTROL -> DEFINE EXPECTED BEHAVIOR -> TEST -> OBSERVE ->
COMPARE -> DETECT DRIFT -> SCORE EFFECTIVENESS -> IDENTIFY GAPS -> RECOMMEND REMEDIATION ->
SIMULATE -> AUTHORIZE -> REMEDIATE -> VERIFY -> CONTINUOUSLY MONITOR.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.security_assurance_fabric_models import (
    SecurityControlDTO,
    SecurityAssertionDTO,
    ControlValidationResultDTO,
    SecurityDriftDTO,
    SecurityBaselineDTO,
    SecurityRegressionRunDTO,
    AIControlAssuranceDTO,
    RemediationPlanDTO,
    SecurityGameDayDTO,
    SecurityDebtDTO,
    AssuranceScorecardDTO,
)
from app.services.assurance_fabric.control_inventory_manager import ControlInventoryManager
from app.services.assurance_fabric.security_assertion_engine import SecurityAssertionEngine
from app.services.assurance_fabric.control_validation_engine import ControlValidationEngine
from app.services.assurance_fabric.security_control_dependency_graph import SecurityControlDependencyGraph
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine
from app.services.assurance_fabric.security_regression_engine import SecurityRegressionEngine
from app.services.assurance_fabric.security_baselines_engine import SecurityBaselinesEngine
from app.services.assurance_fabric.negative_testing_engine import NegativeTestingEngine
from app.services.assurance_fabric.ai_control_assurance_engine import AIControlAssuranceEngine
from app.services.assurance_fabric.model_assurance_engine import ModelAssuranceEngine
from app.services.assurance_fabric.remediation_engine import RemediationEngine
from app.services.assurance_fabric.security_gameday_engine import SecurityGameDayEngine
from app.services.assurance_fabric.security_debt_engine import SecurityDebtEngine
from app.services.assurance_fabric.continuous_assurance_scheduler import ContinuousAssuranceScheduler
from app.services.assurance_fabric.control_effectiveness_scorer import ControlEffectivenessScorer


class SecurityAssuranceFabric:
    """Master Continuous Security Assurance & Control Validation Coordinator for TruthShield X."""

    def __init__(self):
        self.control_manager = ControlInventoryManager()
        self.assertion_engine = SecurityAssertionEngine()
        self.validation_engine = ControlValidationEngine()
        self.dependency_graph = SecurityControlDependencyGraph()
        self.drift_engine = SecurityDriftEngine()
        self.regression_engine = SecurityRegressionEngine()
        self.baselines_engine = SecurityBaselinesEngine()
        self.negative_testing_engine = NegativeTestingEngine()
        self.ai_assurance_engine = AIControlAssuranceEngine()
        self.model_assurance_engine = ModelAssuranceEngine()
        self.remediation_engine = RemediationEngine()
        self.gameday_engine = SecurityGameDayEngine()
        self.debt_engine = SecurityDebtEngine()
        self.scheduler = ContinuousAssuranceScheduler()
        self.scorer = ControlEffectivenessScorer()

    def get_complete_assurance_overview(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        """Provides an aggregated overview of organizational continuous security assurance."""
        controls = self.control_manager.list_controls(tenant_id)
        critical_controls = [c for c in controls if c.criticality == "CRITICAL"]
        validated_controls = [c for c in controls if c.validation_status == "PASS"]
        unverified_controls = [c for c in controls if c.validation_status in ["NOT_VERIFIED", "FAIL"]]
        drifts = self.drift_engine.list_drifts(tenant_id)
        gamedays = self.gameday_engine.list_gamedays(tenant_id)
        debt = self.debt_engine.evaluate_debt(
            unverified_controls=len(unverified_controls),
            tenant_id=tenant_id
        )
        scorecard = self.scorer.evaluate_scorecard(
            tenant_id=tenant_id,
            drift_count=len([d for d in drifts if not d.is_reconciled])
        )

        return {
            "tenant_id": tenant_id,
            "security_controls_count": len(controls),
            "critical_controls_count": len(critical_controls),
            "validated_controls_count": len(validated_controls),
            "unverified_controls_count": len(unverified_controls),
            "active_drifts_count": len([d for d in drifts if not d.is_reconciled]),
            "game_days_count": len(gamedays),
            "security_debt_score": debt.total_debt_score,
            "overall_assurance_score": scorecard.overall_score,
            "assurance_maturity": scorecard.maturity_level,
            "scorecard_grade": scorecard.scorecard_grade,
            "residual_risk_score": scorecard.residual_risk_score,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
