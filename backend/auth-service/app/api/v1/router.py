from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, health, dashboard, scan, audio, apk, notifications, reports, network, storage, dataflow, behavior, threat_intelligence, rules, evidence, risk, rendering, investigation, intelligence, monitoring, soc, governance, response_orchestration, knowledge, threat_predictive, exposure, security_ops, federated_intelligence, autonomous_hunting, digital_twin, assurance, governance_fabric, mission_control, collective_defense, adaptive_defense, cyber_resilience_twin, knowledge_fabric, copilot, soc_orchestration, threat_intelligence_fabric, cyber_resilience, assurance_fabric, security_engineering, digital_twin_lab, global_intelligence, global_defense, mission_control_os, autonomous_defense, ai_governance, enterprise_compliance, threat_intelligence_fusion, zero_trust_exposure, cyber_digital_twin, cyber_crisis_copilot, continuous_operations, continuous_assurance, release_guardian

api_router = APIRouter()
api_router.include_router(continuous_operations.router)
api_router.include_router(continuous_assurance.router)
api_router.include_router(release_guardian.router)



api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(health.router)
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(scan.router, prefix="/scan", tags=["Scan"])
api_router.include_router(audio.router, prefix="/audio", tags=["Audio Scan & Voice Clone AI"])
api_router.include_router(apk.router, prefix="/apk", tags=["Android APK Security AI"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(rendering.router, prefix="/reports", tags=["Report Rendering & Export"])
api_router.include_router(investigation.router, tags=["Investigation Workspace"])
api_router.include_router(intelligence.router, tags=["Unified Trust Intelligence Graph Engine"])
api_router.include_router(monitoring.router, tags=["Real-Time Trust Monitoring & Continuous Intelligence"])
api_router.include_router(soc.router)
api_router.include_router(governance.router)
api_router.include_router(response_orchestration.router)
api_router.include_router(knowledge.router)
api_router.include_router(threat_predictive.router)
api_router.include_router(exposure.router)
api_router.include_router(security_ops.router)
api_router.include_router(federated_intelligence.router)
api_router.include_router(autonomous_hunting.router)
api_router.include_router(digital_twin.router)
api_router.include_router(assurance.router)
api_router.include_router(governance_fabric.router)
api_router.include_router(mission_control.router)
api_router.include_router(collective_defense.router)
api_router.include_router(adaptive_defense.router)
api_router.include_router(cyber_resilience_twin.router)
api_router.include_router(knowledge_fabric.router)
api_router.include_router(copilot.router)
api_router.include_router(soc_orchestration.router)
api_router.include_router(threat_intelligence_fabric.router)
api_router.include_router(cyber_resilience.router)
api_router.include_router(assurance_fabric.router)
api_router.include_router(security_engineering.router)
api_router.include_router(digital_twin_lab.router)
api_router.include_router(global_intelligence.router)
api_router.include_router(global_defense.router)
api_router.include_router(mission_control_os.router)
api_router.include_router(autonomous_defense.router)
api_router.include_router(ai_governance.router)
api_router.include_router(enterprise_compliance.router)
api_router.include_router(threat_intelligence_fusion.router)
api_router.include_router(zero_trust_exposure.router)
api_router.include_router(cyber_digital_twin.router)
api_router.include_router(cyber_crisis_copilot.router)



api_router.include_router(network.router)
api_router.include_router(storage.router)
api_router.include_router(dataflow.router)
api_router.include_router(behavior.router)
api_router.include_router(threat_intelligence.router)
api_router.include_router(rules.router)
api_router.include_router(evidence.router)
api_router.include_router(risk.router)







