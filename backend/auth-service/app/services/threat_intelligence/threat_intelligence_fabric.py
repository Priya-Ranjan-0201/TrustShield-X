"""
TruthShield X — Master Threat Intelligence Fabric (Phase 22).

The unified orchestrator connecting heterogeneous feed ingestion, normalization, deduplication,
graph traversal, campaign discovery, local relevance, early warnings, forecasting, and collaborative defense.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.threat_intelligence_fabric_models import (
    IntelligenceSourceDTO,
    FeedHealthDTO,
    ThreatIntelligenceObjectDTO,
    ThreatIntelligenceGraphDTO,
    CampaignClusterDTO,
    LocalThreatRelevanceDTO,
    ThreatEarlyWarningDTO,
    ThreatForecastDTO,
    CollaborativeContributionDTO,
    IntelligenceDisputeDTO,
    IntelligenceRevocationDTO,
    IntelligenceQualityMetricsDTO,
)
from app.services.threat_intelligence.intelligence_source_manager import IntelligenceSourceManager
from app.services.threat_intelligence.feed_health_engine import FeedHealthEngine
from app.services.threat_intelligence.intelligence_normalization_engine import IntelligenceNormalizationEngine
from app.services.threat_intelligence.intelligence_deduplication_engine import IntelligenceDeduplicationEngine
from app.services.threat_intelligence.entity_resolution_engine import EntityResolutionEngine
from app.services.threat_intelligence.threat_intelligence_graph_engine import ThreatIntelligenceGraphEngine
from app.services.threat_intelligence.corroboration_contradiction_engine import CorroborationContradictionEngine
from app.services.threat_intelligence.campaign_discovery_engine import CampaignDiscoveryEngine
from app.services.threat_intelligence.campaign_evolution_engine import CampaignEvolutionEngine
from app.services.threat_intelligence.local_threat_relevance_engine import LocalThreatRelevanceEngine
from app.services.threat_intelligence.early_warning_engine import ThreatEarlyWarningEngine
from app.services.threat_intelligence.threat_forecast_engine import ThreatForecastEngine
from app.services.threat_intelligence.intelligence_operationalization_engine import IntelligenceOperationalizationEngine
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine
from app.services.threat_intelligence.intelligence_quality_engine import IntelligenceQualityEngine


class ThreatIntelligenceFabric:
    """Master Coordinator for Global Cyber Threat Intelligence Fusion & Collaborative Defense."""

    def __init__(self):
        self.sources = IntelligenceSourceManager()
        self.feed_health = FeedHealthEngine()
        self.normalization = IntelligenceNormalizationEngine()
        self.deduplication = IntelligenceDeduplicationEngine()
        self.entity_resolution = EntityResolutionEngine()
        self.graph = ThreatIntelligenceGraphEngine()
        self.corroboration = CorroborationContradictionEngine()
        self.campaigns = CampaignDiscoveryEngine()
        self.evolution = CampaignEvolutionEngine()
        self.relevance = LocalThreatRelevanceEngine()
        self.early_warning = ThreatEarlyWarningEngine()
        self.forecast = ThreatForecastEngine()
        self.operationalization = IntelligenceOperationalizationEngine()
        self.collaboration = CollaborativeDefenseEngine()
        self.quality = IntelligenceQualityEngine()

        self._objects: Dict[str, ThreatIntelligenceObjectDTO] = {}
        self._seed_objects()

    def _seed_objects(self):
        o1 = ThreatIntelligenceObjectDTO(
            object_id="tio_ind_c2_shadow",
            tenant_id="default_tenant",
            object_type="DOMAIN",
            value="c2.shadowhydra.net",
            canonical_value="c2.shadowhydra.net",
            source_id="src_crowdstrike_falcon",
            confidence=0.96,
            status="ACTIVE",
            classification="COMMUNITY",
        )
        o2 = ThreatIntelligenceObjectDTO(
            object_id="tio_ind_ip_shadow",
            tenant_id="default_tenant",
            object_type="IP",
            value="198.51.100.42",
            canonical_value="198.51.100.42",
            source_id="src_misp_cve",
            confidence=0.92,
            status="ACTIVE",
            classification="PUBLIC",
        )
        self._objects[o1.object_id] = o1
        self._objects[o2.object_id] = o2

    def ingest_raw_intelligence(
        self,
        raw_data: Dict[str, Any],
        source_id: str,
        tenant_id: str = "default_tenant",
        feed_format: str = "STIX2",
    ) -> Dict[str, Any]:
        """Ingests, normalizes, deduplicates, and resolves raw threat feed items."""
        # 1. Normalize
        norm_obj = self.normalization.normalize(raw_data, source_id, tenant_id, feed_format)

        # 2. Entity Resolution
        res = self.entity_resolution.resolve_entity(norm_obj.value, norm_obj.object_type)

        # 3. Deduplicate
        dedup_info = self.deduplication.process_object(norm_obj)

        self._objects[norm_obj.object_id] = norm_obj

        return {
            "object": norm_obj,
            "resolved_entity": res,
            "deduplication": dedup_info,
        }

    def search_intelligence(self, query: str, tenant_id: str = "default_tenant") -> List[ThreatIntelligenceObjectDTO]:
        q = query.lower().strip()
        return [
            obj for obj in self._objects.values()
            if (obj.tenant_id in (tenant_id, "default_tenant") or obj.classification in ("PUBLIC", "COMMUNITY"))
            and (q in obj.canonical_value or q in obj.object_type.lower())
        ]

    def get_object(self, object_id: str) -> Optional[ThreatIntelligenceObjectDTO]:
        return self._objects.get(object_id)
