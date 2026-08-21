"""
TruthShield X — AI Security & Governance Engine (Phase 31 Master Coordinator).

Unified AI Trust, Security, and Governance Control Plane coordinating model lifecycle,
prompt defenses, RAG trust evaluation, agent permissions, and adversarial red-teaming.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.ai_security_governance_models import (
    AIAssetDTO,
    ModelRegistryDTO,
    DatasetDTO,
    PromptTemplateDTO,
    AIAgentDTO,
    ToolRegistryDTO,
    AIIncidentDTO,
    AIRedTeamResultDTO,
    AIRiskScorecardDTO,
)
from app.services.ai_governance.ai_asset_inventory_engine import AIAssetInventoryEngine
from app.services.ai_governance.model_registry_engine import ModelRegistryEngine
from app.services.ai_governance.model_supply_chain_engine import ModelSupplyChainEngine
from app.services.ai_governance.dataset_governance_engine import DatasetGovernanceEngine
from app.services.ai_governance.secure_rag_engine import SecureRAGEngine
from app.services.ai_governance.prompt_security_engine import PromptSecurityEngine
from app.services.ai_governance.ai_agent_security_engine import AIAgentSecurityEngine
from app.services.ai_governance.ai_tool_governance_engine import AIToolGovernanceEngine
from app.services.ai_governance.ai_output_validation_engine import AIOutputValidationEngine
from app.services.ai_governance.model_behavior_monitoring_engine import ModelBehaviorMonitoringEngine
from app.services.ai_governance.ai_incident_response_engine import AIIncidentResponseEngine
from app.services.ai_governance.ai_provider_governance_engine import AIProviderGovernanceEngine
from app.services.ai_governance.ai_red_team_engine import AIRedTeamEngine
from app.services.ai_governance.ai_risk_scorecard_engine import AIRiskScorecardEngine
from app.services.ai_governance.ai_tenant_privacy_engine import AITenantPrivacyEngine


class AISecurityGovernanceEngine:
    """Master AI Security and Model Governance Control Plane Coordinator."""

    def __init__(self):
        self.asset_engine = AIAssetInventoryEngine()
        self.model_engine = ModelRegistryEngine()
        self.supply_chain_engine = ModelSupplyChainEngine()
        self.dataset_engine = DatasetGovernanceEngine()
        self.rag_engine = SecureRAGEngine()
        self.prompt_engine = PromptSecurityEngine()
        self.agent_engine = AIAgentSecurityEngine()
        self.tool_engine = AIToolGovernanceEngine()
        self.output_engine = AIOutputValidationEngine()
        self.behavior_engine = ModelBehaviorMonitoringEngine()
        self.incident_engine = AIIncidentResponseEngine()
        self.provider_engine = AIProviderGovernanceEngine()
        self.red_team_engine = AIRedTeamEngine()
        self.risk_engine = AIRiskScorecardEngine()
        self.privacy_engine = AITenantPrivacyEngine()

    def get_governance_summary(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        assets = self.asset_engine.list_assets(tenant_id)
        models = self.model_engine.list_models()
        prompts = self.prompt_engine.list_prompts()
        agents = self.agent_engine.list_agents()
        incidents = self.incident_engine.list_incidents(tenant_id)
        scorecard = self.risk_engine.evaluate_ai_risk()

        return {
            "total_assets": len(assets),
            "registered_models": len(models),
            "approved_models": len([m for m in models if m.approval_status == "APPROVED"]),
            "quarantined_models": len([m for m in models if m.deployment_status == "QUARANTINED"]),
            "prompt_templates": len(prompts),
            "ai_agents": len(agents),
            "ai_incidents_blocked": len(incidents),
            "overall_ai_risk": scorecard.overall_risk_level,
            "system_health": "HEALTHY",
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
