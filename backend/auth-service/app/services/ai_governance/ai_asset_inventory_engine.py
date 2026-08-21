"""
TruthShield X — AI Asset Inventory Engine (Phase 31).

Manages the comprehensive asset inventory across LLMs, classifiers, embeddings, agents, tools, and RAG pipelines.
"""

from typing import Dict, List, Optional
from app.schemas.ai_security_governance_models import AIAssetDTO, AIAssetTypeLiteral


class AIAssetInventoryEngine:
    """Central registry and inventory tracker for all AI/ML assets across TruthShield X."""

    def __init__(self):
        self._assets: Dict[str, AIAssetDTO] = {}
        self._seed_default_assets()

    def _seed_default_assets(self):
        a1 = AIAssetDTO(
            asset_id="ai_ast_c2_classifier",
            name="Multi-Modal Threat Classifier",
            type="CLASSIFIER",
            owner="AI_SECURITY_TEAM",
            version="2.1.0",
            provider="INTERNAL_SECURE_ENCLAVE",
            deployment="Production Kubernetes Cluster",
            environment="PRODUCTION",
            purpose="Real-time threat classification & C2 detection",
            tenant_scope="default_tenant",
            classification="CONFIDENTIAL",
            status="ACTIVE",
        )
        a2 = AIAssetDTO(
            asset_id="ai_ast_copilot_llm",
            name="Security Copilot Reasoning Engine",
            type="LLM",
            owner="SOC_AUTOMATION_LEAD",
            version="3.5.0",
            provider="INTERNAL_SECURE_ENCLAVE",
            deployment="Isolated Inference Enclave",
            environment="PRODUCTION",
            purpose="Security incident investigation & synthesis",
            tenant_scope="default_tenant",
            classification="RESTRICTED",
            status="ACTIVE",
        )
        self._assets[a1.asset_id] = a1
        self._assets[a2.asset_id] = a2

    def register_asset(self, asset: AIAssetDTO) -> AIAssetDTO:
        self._assets[asset.asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> Optional[AIAssetDTO]:
        return self._assets.get(asset_id)

    def list_assets(self, tenant_id: str = "default_tenant") -> List[AIAssetDTO]:
        return [a for a in self._assets.values() if a.tenant_scope == tenant_id]
