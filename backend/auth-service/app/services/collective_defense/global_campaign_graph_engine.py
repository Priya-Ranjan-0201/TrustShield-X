"""
TruthShield X — Global Campaign Graph & Multi-Modal Fusion Engine (Phase 16).

Maintains privacy-safe cross-tenant campaign graph, clusters multi-modal attack
patterns (phishing, voice, deepfake, APK, QR, payment), and computes campaign confidence.
"""

from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timezone
import uuid

from app.schemas.collective_defense_models import (
    GlobalCampaignGraphDTO,
    GlobalCampaignNodeDTO,
    GlobalCampaignEdgeDTO,
    GlobalCampaignDetailDTO,
    ThreatIntelligenceObjectDTO,
    AttributionStatusLiteral,
)


class GlobalCampaignGraphEngine:
    """Manages the global privacy-preserving campaign knowledge graph."""

    def __init__(self):
        self._nodes: Dict[str, GlobalCampaignNodeDTO] = {}
        self._edges: Dict[str, GlobalCampaignEdgeDTO] = {}
        self._campaigns: Dict[str, GlobalCampaignDetailDTO] = {}

    def add_or_update_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        confidence: float = 0.80,
    ) -> GlobalCampaignNodeDTO:
        """Adds or updates a graph node."""
        node = GlobalCampaignNodeDTO(
            node_id=node_id,
            node_type=node_type,  # type: ignore
            label=label,
            properties=properties or {},
            confidence=confidence,
        )
        self._nodes[node_id] = node
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        confidence: float = 0.75,
    ) -> GlobalCampaignEdgeDTO:
        """Connects two nodes with a typed relationship edge."""
        edge = GlobalCampaignEdgeDTO(
            source_node_id=source_id,
            target_node_id=target_id,
            relationship=relationship,  # type: ignore
            confidence=confidence,
        )
        self._edges[edge.edge_id] = edge
        return edge

    def cluster_campaign(
        self,
        name: str,
        indicators: List[ThreatIntelligenceObjectDTO],
        modalities: Optional[List[str]] = None,
        attributed_actor: Optional[str] = None,
        actor_evidence: Optional[List[str]] = None,
    ) -> GlobalCampaignDetailDTO:
        """Clusters related multi-modal indicators into a Campaign."""
        campaign_id = f"gcmp_{uuid.uuid4().hex[:8]}"

        # 1. Multi-modal synthesis
        all_modalities = set(modalities or [])
        cohorts = set()
        for obj in indicators:
            if obj.intelligence_type in ("VOICE_SIGNATURE",):
                all_modalities.add("VOICE_CLONE")
            elif obj.intelligence_type in ("QR_INDICATOR",):
                all_modalities.add("QR_PHISHING")
            elif obj.intelligence_type in ("APK_SIGNATURE",):
                all_modalities.add("MALICIOUS_APK")
            elif obj.intelligence_type in ("PAYMENT_IDENTIFIER",):
                all_modalities.add("FINANCIAL_FRAUD")
            else:
                all_modalities.add("NETWORK_INFRASTRUCTURE")

            if obj.anonymized_tenant_cohort:
                cohorts.add(obj.anonymized_tenant_cohort)

        # 2. Campaign confidence calculation (Section 32 - multiple independent sources boost confidence)
        unique_sources = {obj.source_id for obj in indicators}
        base_confidence = min(0.95, 0.50 + 0.10 * len(unique_sources) + 0.05 * len(all_modalities))

        # 3. Attribution Safety (Section 33 - default ATTRIBUTION_UNCONFIRMED)
        attribution_status: AttributionStatusLiteral = "ATTRIBUTION_UNCONFIRMED"
        if attributed_actor and actor_evidence and len(actor_evidence) >= 2:
            attribution_status = "PLAUSIBLE"

        campaign = GlobalCampaignDetailDTO(
            campaign_id=campaign_id,
            name=name,
            confidence=round(base_confidence, 2),
            attribution_status=attribution_status,
            attributed_actor=attributed_actor if attribution_status != "ATTRIBUTION_UNCONFIRMED" else None,
            attribution_evidence=actor_evidence or [],
            indicators=[o.canonical_identifier for o in indicators],
            infrastructure_nodes=[o.canonical_identifier for o in indicators if o.intelligence_type in ("DOMAIN", "IP", "URL")],
            modalities=list(all_modalities),
            affected_cohorts=list(cohorts),
            expansion_velocity=float(len(indicators)),
            expansion_warning=len(indicators) >= 5 or len(all_modalities) >= 3,
            supporting_sources_count=len(unique_sources),
        )

        self._campaigns[campaign_id] = campaign

        # Graph node & edges
        self.add_or_update_node(campaign_id, "CAMPAIGN", name, {"modalities": list(all_modalities)}, base_confidence)
        for obj in indicators:
            node_id = f"ind_{obj.content_hash[:8]}"
            self.add_or_update_node(node_id, "INDICATOR", obj.canonical_identifier, {"type": obj.intelligence_type})
            self.add_edge(node_id, campaign_id, "CAMPAIGN_ASSOCIATION", base_confidence)

        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[GlobalCampaignDetailDTO]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self) -> List[GlobalCampaignDetailDTO]:
        return list(self._campaigns.values())

    def export_graph(self) -> GlobalCampaignGraphDTO:
        return GlobalCampaignGraphDTO(
            nodes=list(self._nodes.values()),
            edges=list(self._edges.values()),
            total_campaigns=len(self._campaigns),
            total_indicators=len([n for n in self._nodes.values() if n.node_type == "INDICATOR"]),
            total_infrastructure_clusters=len([n for n in self._nodes.values() if n.node_type == "INFRASTRUCTURE"]),
        )
