"""
TruthShield X — Change Impact & Blast Radius Analysis Engine (Phase 25).

Calculates blast radius and risk classifications to prevent unintended side effects from automated changes.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import ImpactAnalysisDTO, ChangeRiskClassificationLiteral


class ChangeImpactAnalysisEngine:
    """Evaluates dependencies, blast radius, and approval requirements for security modifications."""

    def __init__(self):
        self._impacts: Dict[str, ImpactAnalysisDTO] = {}

    def analyze_impact(
        self,
        improvement_id: str,
        affected_controls: Optional[List[str]] = None,
        affected_services: Optional[List[str]] = None,
        affected_tenants: Optional[List[str]] = None,
        affected_policies: Optional[List[str]] = None,
        affected_detections: Optional[List[str]] = None,
        affected_playbooks: Optional[List[str]] = None,
        affected_recovery_paths: Optional[List[str]] = None,
    ) -> ImpactAnalysisDTO:
        ctrls = affected_controls or ["ctl_tenant_isolation"]
        srvs = affected_services or ["app_auth_service"]
        tenants = affected_tenants or ["default_tenant"]

        # Blast radius score based on breadth of impact
        blast_radius = min(1.0, round((len(ctrls) * 0.05) + (len(srvs) * 0.05) + (len(tenants) * 0.1), 2))

        # Risk Classification
        if blast_radius > 0.5 or len(tenants) > 3:
            risk_class: ChangeRiskClassificationLiteral = "HIGH_RISK"
            requires_human = True
        elif blast_radius > 0.25:
            risk_class = "MODERATE_RISK"
            requires_human = True
        else:
            risk_class = "LOW_RISK_REVERSIBLE"
            requires_human = False

        dto = ImpactAnalysisDTO(
            improvement_id=improvement_id,
            affected_controls=ctrls,
            affected_services=srvs,
            affected_tenants=tenants,
            affected_policies=affected_policies or [],
            affected_detections=affected_detections or ["rule_sigma_t1055"],
            affected_playbooks=affected_playbooks or [],
            affected_recovery_paths=affected_recovery_paths or [],
            blast_radius_score=blast_radius,
            risk_classification=risk_class,
            requires_human_approval=requires_human,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._impacts[dto.impact_id] = dto
        return dto

    def get_impact(self, impact_id: str) -> Optional[ImpactAnalysisDTO]:
        return self._impacts.get(impact_id)
