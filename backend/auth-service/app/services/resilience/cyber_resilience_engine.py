"""
TruthShield X — Cyber Resilience Engine (Phase 23 Master Coordinator).

Orchestrates the complete 14-stage resilience lifecycle:
ASSESS -> MODEL -> SIMULATE -> IDENTIFY FAILURE -> PLAN RECOVERY -> AUTHORIZE ->
EXECUTE -> VERIFY -> RESTORE -> VALIDATE -> MEASURE -> LEARN -> IMPROVE -> RE-VALIDATE.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.cyber_resilience_models import (
    ResilienceAssetDTO,
    BusinessServiceDTO,
    ServiceDependencyGraphDTO,
    ResilienceGapDTO,
    BackupValidationDTO,
    RTOEngineDTO,
    RPOEngineDTO,
    RecoveryPlanDTO,
    RecoveryActionExecutionDTO,
    RecoveryVerificationDTO,
    BusinessValidationResultDTO,
    DisasterRecoveryDrillDTO,
    RecoveryDriftDTO,
    ResilienceScorecardDTO,
)
from app.services.resilience.resilience_asset_manager import ResilienceAssetManager
from app.services.resilience.resilience_dependency_graph_engine import ResilienceDependencyGraphEngine
from app.services.resilience.resilience_gap_engine import ResilienceGapEngine
from app.services.resilience.backup_validation_engine import BackupValidationEngine
from app.services.resilience.rpo_rto_engine import RPORTOEngine
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine
from app.services.resilience.recovery_execution_engine import RecoveryExecutionEngine
from app.services.resilience.recovery_verification_engine import RecoveryVerificationEngine
from app.services.resilience.business_validation_engine import BusinessValidationEngine
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine
from app.services.resilience.resilience_drift_engine import ResilienceDriftEngine
from app.services.resilience.continuous_resilience_validation_engine import ContinuousResilienceValidationEngine
from app.services.resilience.resilience_score_engine import ResilienceScoreEngine
from app.services.resilience.resilience_digital_twin_engine import ResilienceDigitalTwinEngine
from app.services.resilience.safe_automated_recovery_engine import SafeAutomatedRecoveryEngine


class CyberResilienceEngine:
    """Master Cyber Resilience & Autonomous Recovery Coordinator for TruthShield X."""

    def __init__(self):
        self.asset_manager = ResilienceAssetManager()
        self.dependency_graph_engine = ResilienceDependencyGraphEngine()
        self.gap_engine = ResilienceGapEngine()
        self.backup_engine = BackupValidationEngine()
        self.rpo_rto_engine = RPORTOEngine()
        self.plan_engine = RecoveryPlanEngine()
        self.execution_engine = RecoveryExecutionEngine()
        self.verification_engine = RecoveryVerificationEngine()
        self.business_validation_engine = BusinessValidationEngine()
        self.drill_engine = DisasterRecoveryDrillEngine()
        self.drift_engine = ResilienceDriftEngine()
        self.continuous_validation_engine = ContinuousResilienceValidationEngine()
        self.score_engine = ResilienceScoreEngine()
        self.twin_engine = ResilienceDigitalTwinEngine()
        self.safety_engine = SafeAutomatedRecoveryEngine()

    def get_complete_resilience_overview(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        """Provides an aggregated overview of organizational cyber resilience."""
        assets = self.asset_manager.list_assets(tenant_id)
        services = self.asset_manager.list_business_services(tenant_id)
        graph = self.dependency_graph_engine.build_graph(tenant_id)
        gaps = self.gap_engine.list_gaps(tenant_id)
        plans = self.plan_engine.list_plans(tenant_id)
        drills = self.drill_engine.list_drills(tenant_id)
        drifts = self.drift_engine.list_drifts(tenant_id)
        scorecard = self.score_engine.evaluate_scorecard(tenant_id)

        return {
            "tenant_id": tenant_id,
            "critical_assets_count": len(assets),
            "critical_services_count": len(services),
            "single_points_of_failure_count": len(graph.single_points_of_failure),
            "unresolved_gaps_count": len([g for g in gaps if g.validation_status == "UNRESOLVED"]),
            "active_plans_count": len(plans),
            "drills_count": len(drills),
            "unreconciled_drift_count": len([d for d in drifts if not d.is_reconciled]),
            "overall_resilience_score": scorecard.overall_score,
            "resilience_maturity": scorecard.maturity_level,
            "scorecard_grade": scorecard.scorecard_grade,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
