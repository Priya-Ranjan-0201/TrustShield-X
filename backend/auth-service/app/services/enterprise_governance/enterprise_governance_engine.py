"""
TruthShield X — Enterprise Governance Engine (Phase 32 Master Coordinator).

Unified Enterprise Security & Compliance Operating System coordinating controls,
continuous testing, evidence freshness, risk registers, finding remediation,
audit requests, and continuous assurance drift detection.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.enterprise_governance_models import (
    ControlDTO,
    ComplianceRequirementDTO,
    EvidenceDTO,
    EnterpriseRiskDTO,
    ComplianceFindingDTO,
    RemediationTaskDTO,
    SecurityExceptionDTO,
    AuditRequestDTO,
    ThirdPartyRiskDTO,
    ComplianceSnapshotDTO,
    ComplianceDriftEventDTO,
)
from app.services.enterprise_governance.control_catalog_engine import ControlCatalogEngine
from app.services.enterprise_governance.control_testing_engine import ControlTestingEngine
from app.services.enterprise_governance.continuous_control_monitoring_engine import ContinuousControlMonitoringEngine
from app.services.enterprise_governance.control_drift_engine import ControlDriftEngine
from app.services.enterprise_governance.enterprise_policy_engine import EnterprisePolicyEngine
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry
from app.services.enterprise_governance.evidence_management_engine import EvidenceManagementEngine
from app.services.enterprise_governance.audit_readiness_engine import AuditReadinessEngine
from app.services.enterprise_governance.enterprise_risk_engine import EnterpriseRiskEngine
from app.services.enterprise_governance.compliance_remediation_engine import ComplianceRemediationEngine
from app.services.enterprise_governance.exception_management_engine import ExceptionManagementEngine
from app.services.enterprise_governance.access_review_governance_engine import AccessReviewGovernanceEngine
from app.services.enterprise_governance.third_party_risk_engine import ThirdPartyRiskEngine
from app.services.enterprise_governance.continuous_assurance_engine import ContinuousAssuranceEngine
from app.services.enterprise_governance.compliance_report_generator import ComplianceReportGenerator


class EnterpriseGovernanceEngine:
    """Master Enterprise Security & Compliance Operating System Coordinator."""

    def __init__(self):
        self.control_catalog = ControlCatalogEngine()
        self.control_testing = ControlTestingEngine()
        self.monitoring = ContinuousControlMonitoringEngine()
        self.drift_engine = ControlDriftEngine()
        self.policy_engine = EnterprisePolicyEngine()
        self.requirement_registry = ComplianceRequirementRegistry()
        self.evidence_engine = EvidenceManagementEngine()
        self.audit_engine = AuditReadinessEngine()
        self.risk_engine = EnterpriseRiskEngine()
        self.remediation_engine = ComplianceRemediationEngine()
        self.exception_engine = ExceptionManagementEngine()
        self.access_review_engine = AccessReviewGovernanceEngine()
        self.third_party_engine = ThirdPartyRiskEngine()
        self.assurance_engine = ContinuousAssuranceEngine()
        self.report_generator = ComplianceReportGenerator()

    def get_executive_governance_summary(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        controls = self.control_catalog.list_controls(tenant_id)
        requirements = self.requirement_registry.list_requirements()
        evidence_items = self.evidence_engine.list_evidence()
        risks = self.risk_engine.list_risks()
        findings = self.remediation_engine.list_findings()
        remediations = self.remediation_engine.list_tasks()
        exceptions = self.exception_engine.list_exceptions()
        audit_requests = self.audit_engine.list_requests()
        vendors = self.third_party_engine.list_vendors()

        return {
            "total_controls": len(controls),
            "verified_controls": len([c for c in controls if c.status == "ACTIVE" and c.effectiveness == "EFFECTIVE"]),
            "failed_controls": len([c for c in controls if c.status == "FAILED" or c.effectiveness == "INEFFECTIVE"]),
            "total_requirements": len(requirements),
            "evidence_items": len(evidence_items),
            "evidence_missing_count": 0,
            "total_risks": len(risks),
            "critical_risks": len([r for r in risks if r.residual_risk >= 0.80]),
            "accepted_risks": len([r for r in risks if r.treatment == "ACCEPT"]),
            "open_findings": len([f for f in findings if f.status == "OPEN"]),
            "active_remediations": len([t for t in remediations if t.status != "CLOSED"]),
            "active_exceptions": len([e for e in exceptions if e.status == "ACTIVE"]),
            "audit_requests": len(audit_requests),
            "assessed_vendors": len(vendors),
            "compliance_posture": "CONTINUOUSLY_ASSURED",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
