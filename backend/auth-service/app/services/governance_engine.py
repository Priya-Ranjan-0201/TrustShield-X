"""Enterprise Governance Engine Master Facade (Phase 4.0 Part 8 — Section 1).

Coordinates RBAC, ABAC, policy enforcement, data classification, retention, legal holds,
privacy workflows, exports, append-only audit trails, compliance mappings, and API keys.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.schemas.governance_models import (
    OrganizationDTO,
    UserLifecycleDTO,
    RoleDTO,
    GovernancePolicyDTO,
    AuthorizationDecisionDTO,
    RetentionPolicyDTO,
    LegalHoldDTO,
    DataDeletionRequestDTO,
    PrivacyRequestDTO,
    DataExportManifestDTO,
    AuditEventDTO,
    ComplianceAssessmentDTO,
    ComplianceReportDTO,
    SessionGovernanceDTO,
    APIKeyMetadataDTO,
    APIKeyCreationResponseDTO,
    GovernancePostureDTO,
    DataClassificationLiteral,
    PolicyTypeLiteral,
)
from app.services.governance.rbac_engine import RBACEngine
from app.services.governance.abac_engine import ABACEngine
from app.services.governance.policy_engine import PolicyEngine
from app.services.governance.policy_simulation_engine import PolicySimulationEngine
from app.services.governance.data_classification_engine import DataClassificationEngine
from app.services.governance.legal_hold_engine import LegalHoldEngine
from app.services.governance.data_retention_engine import DataRetentionEngine
from app.services.governance.data_deletion_engine import DataDeletionEngine
from app.services.governance.privacy_request_engine import PrivacyRequestEngine
from app.services.governance.data_export_engine import DataExportEngine
from app.services.governance.audit_service import AuditService
from app.services.governance.audit_intelligence_engine import AuditIntelligenceEngine
from app.services.governance.compliance_engine import ComplianceEngine
from app.services.governance.governance_posture_engine import GovernancePostureEngine
from app.services.governance.session_governance_service import SessionGovernanceService
from app.services.governance.api_key_service import APIKeyService


class GovernanceEngine:
    """Master facade for TruthShield X Enterprise Governance, Authorization, and Compliance."""

    def __init__(self):
        self.rbac_engine = RBACEngine()
        self.abac_engine = ABACEngine()
        self.policy_engine = PolicyEngine()
        self.simulation_engine = PolicySimulationEngine()
        self.classification_engine = DataClassificationEngine()
        self.legal_hold_engine = LegalHoldEngine()
        self.retention_engine = DataRetentionEngine(self.legal_hold_engine)
        self.deletion_engine = DataDeletionEngine(self.legal_hold_engine)
        self.privacy_engine = PrivacyRequestEngine(self.legal_hold_engine)
        self.export_engine = DataExportEngine()
        self.audit_service = AuditService()
        self.audit_intelligence = AuditIntelligenceEngine()
        self.compliance_engine = ComplianceEngine()
        self.posture_engine = GovernancePostureEngine()
        self.session_service = SessionGovernanceService()
        self.api_key_service = APIKeyService()
        self._organizations: Dict[str, OrganizationDTO] = {}
        self._users: Dict[str, UserLifecycleDTO] = {}

    def register_organization(self, name: str, slug: str) -> OrganizationDTO:
        org = OrganizationDTO(organization_name=name, slug=slug)
        self._organizations[org.organization_id] = org
        return org

    def register_user(self, organization_id: str, email: str, roles: List[str]) -> UserLifecycleDTO:
        user = UserLifecycleDTO(organization_id=organization_id, email=email, roles=roles)
        self._users[user.user_id] = user
        return user

    def authorize_request(
        self,
        user_id: str,
        user_roles: List[str],
        user_organization_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        resource_organization_id: Optional[str] = None,
        classification: DataClassificationLiteral = "INTERNAL",
        resource_owner_id: Optional[str] = None,
        incident_severity: Optional[str] = None,
        mfa_verified: bool = False,
        mfa_required_by_policy: bool = False,
        session_status: str = "ACTIVE",
    ) -> AuthorizationDecisionDTO:
        """Comprehensive authorization evaluating Multi-Tenancy, RBAC, ABAC, and Policies (Sections 18, 92-95)."""
        res_org = resource_organization_id or user_organization_id

        # 1. Multi-Tenant Isolation (Section 4, Mandatory Tests 1, 2)
        if res_org != user_organization_id and "SUPER_ADMIN" not in user_roles:
            decision = AuthorizationDecisionDTO(
                allowed=False,
                decision="DENY",
                reason="Access denied: Cross-tenant resource access is strictly prohibited.",
                required_permissions=[f"{resource_type}:{action}"],
            )
            self.audit_service.record_event(
                organization_id=user_organization_id,
                actor_id=user_id,
                action=f"{resource_type}:{action}",
                resource_type=resource_type,
                resource_id=resource_id,
                result="DENIED",
                reason=decision.reason,
            )
            return decision

        # 2. RBAC Permission Check
        rbac_dec = self.rbac_engine.evaluate_rbac_access(
            user_id=user_id,
            user_roles=user_roles,
            resource=resource_type,
            action=action,
            resource_org_id=res_org,
            user_org_id=user_organization_id,
        )
        if not rbac_dec.allowed:
            self.audit_service.record_event(
                organization_id=user_organization_id,
                actor_id=user_id,
                action=f"{resource_type}:{action}",
                resource_type=resource_type,
                resource_id=resource_id,
                result="DENIED",
                reason=rbac_dec.reason,
            )
            return rbac_dec

        # 3. ABAC Context Check
        abac_dec = self.abac_engine.evaluate_abac(
            user_id=user_id,
            user_roles=user_roles,
            resource_id=resource_id,
            resource_type=resource_type,
            classification=classification,
            resource_owner_id=resource_owner_id,
            incident_severity=incident_severity,
            mfa_verified=mfa_verified,
            mfa_required_by_policy=mfa_required_by_policy,
            session_status=session_status,
        )
        if not abac_dec.allowed:
            self.audit_service.record_event(
                organization_id=user_organization_id,
                actor_id=user_id,
                action=f"{resource_type}:{action}",
                resource_type=resource_type,
                resource_id=resource_id,
                result=abac_dec.decision,
                reason=abac_dec.reason,
            )
            return abac_dec

        # 4. Organization Governance Policy Evaluation (Section 18)
        pol_dec = self.policy_engine.evaluate_policies(
            organization_id=user_organization_id,
            user_id=user_id,
            user_roles=user_roles,
            resource=resource_type,
            action=action,
        )
        if not pol_dec.allowed:
            self.audit_service.record_event(
                organization_id=user_organization_id,
                actor_id=user_id,
                action=f"{resource_type}:{action}",
                resource_type=resource_type,
                resource_id=resource_id,
                result=pol_dec.decision,
                reason=pol_dec.reason,
            )
            return pol_dec

        # Success - Audited and Allowed
        self.audit_service.record_event(
            organization_id=user_organization_id,
            actor_id=user_id,
            action=f"{resource_type}:{action}",
            resource_type=resource_type,
            resource_id=resource_id,
            result="SUCCESS",
            reason="Authorized by RBAC/ABAC and Governance Policy.",
        )

        return AuthorizationDecisionDTO(
            allowed=True,
            decision="ALLOW",
            reason="Authorized by RBAC/ABAC and Governance Policy.",
            matched_rules=pol_dec.matched_rules,
        )
