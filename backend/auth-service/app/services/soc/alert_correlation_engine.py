"""SOC Alert Correlation & Clustering Engine (Phase 4.0 Part 7 — Sections 6-10).

Correlates incoming security alerts into coherent clusters, applying modular rules
and enforcing strict false-correlation safeguards against infrastructure overlap.
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime, timezone
from app.schemas.soc_operations_models import (
    SOCAlertDTO,
    AlertClusterDTO,
    ClusterTypeLiteral,
)
from app.services.soc.soc_correlation_rules import (
    AlertEntityRule,
    CampaignRule,
    AttackChainRule,
    TemporalRule,
    CrossModalRule,
)


class SOCAlertCorrelationEngine:
    """Correlates alerts and clusters them into incident candidates."""

    def __init__(self):
        self._clusters: Dict[str, AlertClusterDTO] = {}
        self._alert_to_cluster: Dict[str, str] = {}

    def correlate_alert(self, alert: SOCAlertDTO, existing_alerts: List[SOCAlertDTO]) -> Optional[AlertClusterDTO]:
        """Evaluate correlation of alert against all existing alerts in the active window."""
        matched_cluster_id = None
        cluster_type: ClusterTypeLiteral = "SAME_ENTITY"
        max_confidence = 0.0

        for other in existing_alerts:
            if other.alert_id == alert.alert_id:
                continue

            # Evaluate rules
            for rule in (CampaignRule, AttackChainRule, AlertEntityRule, CrossModalRule, TemporalRule):
                res = rule.evaluate(alert, other)
                if res and res["confidence"] > max_confidence:
                    max_confidence = res["confidence"]
                    cluster_type = res["cluster_type"]
                    # Check if other alert already belongs to a cluster
                    if other.alert_id in self._alert_to_cluster:
                        matched_cluster_id = self._alert_to_cluster[other.alert_id]
                    break

        if max_confidence == 0.0:
            return None  # No valid correlation found

        now_str = datetime.now(timezone.utc).isoformat()

        if matched_cluster_id and matched_cluster_id in self._clusters:
            cluster = self._clusters[matched_cluster_id]
            if alert.alert_id not in cluster.alert_ids:
                cluster.alert_ids.append(alert.alert_id)
            for ent in alert.entity_ids:
                if ent not in cluster.entity_ids:
                    cluster.entity_ids.append(ent)
            cluster.last_seen = now_str
            self._alert_to_cluster[alert.alert_id] = cluster.cluster_id
            return cluster

        # Create new cluster
        cluster = AlertClusterDTO(
            cluster_id=f"clst_{uuid.uuid4().hex[:12]}",
            alert_ids=[alert.alert_id],
            entity_ids=list(set(alert.entity_ids)),
            campaign_id=alert.campaign_id,
            confidence=max_confidence,
            cluster_type=cluster_type,
            first_seen=alert.first_seen,
            last_seen=now_str,
            organization_id=alert.organization_id,
        )
        self._clusters[cluster.cluster_id] = cluster
        self._alert_to_cluster[alert.alert_id] = cluster.cluster_id
        return cluster

    def get_cluster(self, cluster_id: str) -> Optional[AlertClusterDTO]:
        return self._clusters.get(cluster_id)

    def list_clusters(self) -> List[AlertClusterDTO]:
        return list(self._clusters.values())
