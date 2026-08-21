"""
TruthShield X - Phase 34: Zero-Trust & Continuous Exposure Package
"""

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
from app.services.zero_trust_exposure.zero_trust_security_engine import ZeroTrustSecurityEngine, zero_trust_security_engine

__all__ = [
    "ContinuousIdentityEngine", "continuous_identity_engine",
    "DeviceTrustEngine", "device_trust_engine",
    "PostureAssessmentEngine", "posture_assessment_engine",
    "SessionSecurityEngine", "session_security_engine",
    "ServiceIdentityEngine", "service_identity_engine",
    "PrivilegeGovernanceEngine", "privilege_governance_engine",
    "IdentityEntitlementEngine", "identity_entitlement_engine",
    "MicrosegmentationEngine", "microsegmentation_engine",
    "ZeroTrustDecisionEngine", "zero_trust_decision_engine",
    "ExternalAttackSurfaceEngine", "external_attack_surface_engine",
    "AssetDiscoveryInventoryEngine", "asset_discovery_inventory_engine",
    "ExposureManagementEngine", "exposure_management_engine",
    "VulnerabilityExposureCorrelationEngine", "vulnerability_exposure_correlation_engine",
    "VulnerabilityPrioritizationEngine", "vulnerability_prioritization_engine",
    "AttackPathAnalysisEngine", "attack_path_analysis_engine",
    "BlastRadiusCalculatorEngine", "blast_radius_calculator_engine",
    "CrownJewelEngine", "crown_jewel_engine",
    "DataClassificationEngine", "data_classification_engine",
    "ContinuousExposureMonitoringEngine", "continuous_exposure_monitoring_engine",
    "RemediationValidationEngine", "remediation_validation_engine",
    "ThreatExposureOrchestrationEngine", "threat_exposure_orchestration_engine",
    "ExposureValidationEngine", "exposure_validation_engine",
    "ExposureScorecardEngine", "exposure_scorecard_engine",
    "SecurityGraphEngine", "security_graph_engine",
    "ZeroTrustSecurityEngine", "zero_trust_security_engine"
]
