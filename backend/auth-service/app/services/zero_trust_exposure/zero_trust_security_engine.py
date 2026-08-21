"""
Zero-Trust & Continuous Exposure Master Coordinator Engine (Phase 34)
====================================================================
Unified orchestration engine connecting:
- Continuous Identity Security
- Device Trust & Posture Assessment
- Real-time Session Security
- M2M Service Identity
- Privilege Governance & JIT Access / Break-Glass
- Identity Entitlement Management (CIEM)
- Micro-segmentation & Trust Zones
- 8D Zero-Trust Access Decisions
- External Attack Surface Management (EASM)
- Asset Discovery & Inventory
- Exposure Management & Finding Tracking
- Vulnerability Exposure Correlation & Prioritization
- Attack Path & Crown Jewel Graph Analysis
- Blast Radius Computation
- Security Graph & Temporal Reconstruction
- Continuous Exposure & Policy Drift Monitoring
- Verified Remediation Validation
- Threat Exposure Orchestration (CTEM)
- Exposure Validation & BAS
- Exposure Scorecard & Zero Trust Maturity
"""

from typing import Dict, Any, List, Optional
import datetime
import uuid

from app.services.zero_trust_exposure.continuous_identity_engine import ContinuousIdentityEngine, continuous_identity_engine
from app.services.zero_trust_exposure.device_trust_engine import DeviceTrustEngine, device_trust_engine
from app.services.zero_trust_exposure.posture_assessment_engine import PostureAssessmentEngine, posture_assessment_engine
from app.services.zero_trust_exposure.session_security_engine import SessionSecurityEngine, session_security_engine
from app.services.zero_trust_exposure.service_identity_engine import ServiceIdentityEngine, service_identity_engine
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine, privilege_governance_engine
from app.services.zero_trust_exposure.identity_entitlement_engine import IdentityEntitlementEngine, identity_entitlement_engine
from app.services.zero_trust_exposure.microsegmentation_engine import MicrosegmentationEngine, microsegmentation_engine
from app.services.zero_trust_exposure.zero_trust_decision_engine import ZeroTrustDecisionEngine, zero_trust_decision_engine
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine, external_attack_surface_engine
from app.services.zero_trust_exposure.asset_discovery_inventory_engine import AssetDiscoveryInventoryEngine, asset_discovery_inventory_engine
from app.services.zero_trust_exposure.exposure_management_engine import ExposureManagementEngine, exposure_management_engine
from app.services.zero_trust_exposure.vulnerability_exposure_correlation_engine import VulnerabilityExposureCorrelationEngine, vulnerability_exposure_correlation_engine
from app.services.zero_trust_exposure.vulnerability_prioritization_engine import VulnerabilityPrioritizationEngine, vulnerability_prioritization_engine
from app.services.zero_trust_exposure.attack_path_analysis_engine import AttackPathAnalysisEngine, attack_path_analysis_engine
from app.services.zero_trust_exposure.blast_radius_calculator_engine import BlastRadiusCalculatorEngine, blast_radius_calculator_engine
from app.services.zero_trust_exposure.crown_jewel_engine import CrownJewelEngine, crown_jewel_engine
from app.services.zero_trust_exposure.data_classification_engine import DataClassificationEngine, data_classification_engine
from app.services.zero_trust_exposure.continuous_exposure_monitoring_engine import ContinuousExposureMonitoringEngine, continuous_exposure_monitoring_engine
from app.services.zero_trust_exposure.remediation_validation_engine import RemediationValidationEngine, remediation_validation_engine
from app.services.zero_trust_exposure.threat_exposure_orchestration_engine import ThreatExposureOrchestrationEngine, threat_exposure_orchestration_engine
from app.services.zero_trust_exposure.exposure_validation_engine import ExposureValidationEngine, exposure_validation_engine
from app.services.zero_trust_exposure.exposure_scorecard_engine import ExposureScorecardEngine, exposure_scorecard_engine
from app.services.zero_trust_exposure.security_graph_engine import SecurityGraphEngine, security_graph_engine


class ZeroTrustSecurityEngine:
    def __init__(self):
        self.identity_engine = continuous_identity_engine
        self.device_engine = device_trust_engine
        self.posture_engine = posture_assessment_engine
        self.session_engine = session_security_engine
        self.service_engine = service_identity_engine
        self.privilege_engine = privilege_governance_engine
        self.entitlement_engine = identity_entitlement_engine
        self.segmentation_engine = microsegmentation_engine
        self.decision_engine = zero_trust_decision_engine
        self.easm_engine = external_attack_surface_engine
        self.asset_inventory_engine = asset_discovery_inventory_engine
        self.exposure_engine = exposure_management_engine
        self.vuln_correlation_engine = vulnerability_exposure_correlation_engine
        self.vuln_prioritization_engine = vulnerability_prioritization_engine
        self.attack_path_engine = attack_path_analysis_engine
        self.blast_radius_engine = blast_radius_calculator_engine
        self.crown_jewel_engine = crown_jewel_engine
        self.data_classification_engine = data_classification_engine
        self.drift_engine = continuous_exposure_monitoring_engine
        self.remediation_engine = remediation_validation_engine
        self.ctem_orchestration_engine = threat_exposure_orchestration_engine
        self.exposure_validation_engine = exposure_validation_engine
        self.scorecard_engine = exposure_scorecard_engine
        self.security_graph = security_graph_engine

    def evaluate_unified_access_request(
        self,
        tenant_id: str,
        subject_id: str,
        device_id: str,
        session_id: str,
        resource_id: str,
        resource_sensitivity: str,
        action: str,
        source_ip: str,
        auth_context: Optional[Dict[str, Any]] = None,
        device_telemetry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        auth_ctx = auth_context or {}
        dev_tel = device_telemetry or {}

        # 1. Identity assessment
        id_eval = self.identity_engine.evaluate_identity_confidence(
            identity_id=subject_id,
            tenant_id=tenant_id,
            current_ip=source_ip,
            device_id=device_id,
            auth_context=auth_ctx
        )

        # 2. Device assessment
        dev_eval = self.device_engine.assess_posture(
            device_id=device_id,
            tenant_id=tenant_id,
            telemetry=dev_tel
        )

        # 3. Session assessment
        sess_eval = self.session_engine.evaluate_session_activity(
            session_id=session_id,
            tenant_id=tenant_id,
            current_ip=source_ip,
            current_device=device_id,
            activity_type=action,
            risk_signals=auth_ctx.get("risk_signals")
        )

        # 4. Composite Risk Calculation
        composite_risk = max(
            id_eval.get("risk_score", 0.0),
            sess_eval.get("risk_score", 0.0),
            10.0 - dev_eval.get("posture_score", 0.0)
        )

        # 5. 8D Zero-Trust Decision
        decision = self.decision_engine.evaluate_access(
            tenant_id=tenant_id,
            correlation_id=f"ZT-CORR-{uuid.uuid4().hex[:8]}",
            subject_id=subject_id,
            device_id=device_id,
            session_id=session_id,
            resource_id=resource_id,
            resource_sensitivity=resource_sensitivity,
            action=action,
            identity_trust_state=id_eval.get("trust_state", "IDENTITY_UNTRUSTED"),
            device_trust_state=dev_eval.get("trust_state", "UNTRUSTED"),
            session_state=sess_eval.get("state", "TERMINATED"),
            risk_score=composite_risk
        )

        return {
            "evaluation_id": decision["decision_id"],
            "decision": decision["decision"],
            "decision_reason": decision["decision_reason"],
            "required_action": decision["required_action"],
            "identity_trust_state": id_eval.get("trust_state"),
            "device_trust_state": dev_eval.get("trust_state"),
            "session_state": sess_eval.get("state"),
            "composite_risk_score": composite_risk,
            "confidence": decision["confidence"],
            "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def generate_trust_scorecard(self, tenant_id: str, subject_id: str) -> Dict[str, Any]:
        ident = self.identity_engine.get_identity(subject_id, tenant_id)
        id_trust = 1.0 if ident and ident.get("identity_trust_state") == "TRUSTED" else 0.5 if ident else 0.0
        
        return {
            "scorecard_id": f"TSC-{uuid.uuid4().hex[:8]}",
            "tenant_id": tenant_id,
            "subject_id": subject_id,
            "identity_trust": id_trust,
            "device_trust": 0.85,
            "session_trust": 0.90,
            "resource_risk": 0.20,
            "exposure_level": 0.15,
            "policy_compliance": 0.98,
            "threat_context_score": 0.05,
            "overall_confidence": round((id_trust + 0.85 + 0.90 + 0.98) / 4.0, 2),
            "evaluated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


# Global singleton instance
zero_trust_security_engine = ZeroTrustSecurityEngine()
