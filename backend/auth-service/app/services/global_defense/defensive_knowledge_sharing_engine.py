"""
TruthShield X — Defensive Knowledge Sharing Engine (Phase 28).

Packages, validates, and shares sanitized defensive techniques, Sigma rules, and mitigation patterns.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.global_defense_models import DefensiveKnowledgeRecordDTO


class DefensiveKnowledgeSharingEngine:
    """Manages sanitized, evidence-backed defensive knowledge records for peer reuse."""

    def __init__(self):
        self._knowledge_base: Dict[str, DefensiveKnowledgeRecordDTO] = {}
        self._seed_default_knowledge()

    def _seed_default_knowledge(self):
        k1 = DefensiveKnowledgeRecordDTO(
            knowledge_id="dknow_darkstorm_dns_rate_limit",
            problem="DarkStorm C2 DNS Tunneling via Ephemeral Port Bursts",
            evidence=["PCAP DNS payload entropy", "NetFlow burst spikes"],
            defensive_technique="Deploy DNS Entropy Detection Sigma Rule & Dynamic Rate-Limiter",
            validation_result="Verified 85% Containment in Phase 26 Digital Twin Lab",
            environment="LINUX_KUBERNETES_CONTAINERS",
            compatibility=["CORE_DNS", "NGINX_INGRESS", "FASTAPI_GW"],
            source_tenant_scope="default_tenant",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._knowledge_base[k1.knowledge_id] = k1

    def publish_knowledge(
        self,
        problem: str,
        evidence: List[str],
        defensive_technique: str,
        validation_result: str,
        compatibility: List[str],
        source_tenant: str = "default_tenant",
    ) -> DefensiveKnowledgeRecordDTO:
        dto = DefensiveKnowledgeRecordDTO(
            problem=problem,
            evidence=evidence,
            defensive_technique=defensive_technique,
            validation_result=validation_result,
            compatibility=compatibility,
            source_tenant_scope=source_tenant,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._knowledge_base[dto.knowledge_id] = dto
        return dto

    def get_knowledge(self, knowledge_id: str) -> Optional[DefensiveKnowledgeRecordDTO]:
        return self._knowledge_base.get(knowledge_id)

    def list_knowledge(self) -> List[DefensiveKnowledgeRecordDTO]:
        return list(self._knowledge_base.values())
