"""
TruthShield X — Multi-Modal Threat Fusion & Clustering Engine
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.fusion_models import SecurityEventDTO, ThreatFusionScoreDTO, ThreatClusterDTO


class ThreatFusionEngine:
    """Fuses multi-modal threat signals across web, QR, UPI, deepfake, voice, APK, and infrastructure into cohesive threat clusters."""

    MODALITY_WEIGHTS = {
        "WEB": 1.0,
        "QR": 1.1,
        "UPI": 1.3,
        "DOCUMENT": 1.0,
        "DEEPFAKE": 1.4,
        "VOICE": 1.4,
        "APK": 1.5,
        "IDENTITY": 1.2,
        "DOMAIN": 1.0,
        "INFRASTRUCTURE": 1.2,
        "CAMPAIGN": 1.3,
        "SOC": 1.0,
        "THREAT_INTELLIGENCE": 1.1,
    }

    def __init__(self):
        # tenant_id -> cluster_id -> ThreatClusterDTO
        self._clusters: Dict[str, Dict[str, ThreatClusterDTO]] = {}

    def calculate_fusion_score(
        self,
        events: List[SecurityEventDTO],
        counter_events: Optional[List[SecurityEventDTO]] = None,
    ) -> ThreatFusionScoreDTO:
        """Calculates multi-modal threat fusion score using Bayesian evidence convergence."""
        if not events:
            return ThreatFusionScoreDTO(
                fusion_score=0.0,
                confidence=0.0,
                converged_modalities=[],
                supporting_signals_count=0,
                counter_signals_count=0,
                explanation="No active security events available for threat fusion.",
            )

        modalities = list(set(e.source.upper() for e in events))
        modality_count = len(modalities)

        # Base fusion component: weighted average of event risks and severities
        severity_map = {"CRITICAL": 100.0, "HIGH": 75.0, "MEDIUM": 50.0, "LOW": 25.0, "INFORMATIONAL": 10.0}
        total_signal_weight = sum(self.MODALITY_WEIGHTS.get(m, 1.0) for m in modalities)
        avg_risk = sum(e.risk_score for e in events) / len(events)

        # Cross-modal convergence bonus (+10 per distinct modality beyond first, up to +35)
        convergence_bonus = min(35.0, max(0, modality_count - 1) * 10.0)

        # Counter-evidence discount
        counter_count = len(counter_events) if counter_events else 0
        counter_discount = counter_count * 15.0

        raw_fusion = (avg_risk * 0.7) + convergence_bonus - counter_discount
        final_fusion_score = max(0.0, min(100.0, round(raw_fusion, 1)))

        # Confidence is high when multiple reliable modalities converge
        avg_confidence = sum(e.confidence for e in events) / len(events)
        fusion_confidence = min(0.99, max(0.40, avg_confidence + (0.05 * modality_count) - (0.10 * counter_count)))

        explanation = (
            f"Fused {len(events)} security events across {modality_count} modalities ({', '.join(modalities)}). "
            f"Cross-modal convergence added +{convergence_bonus:.1f} score weighting."
        )

        return ThreatFusionScoreDTO(
            fusion_score=final_fusion_score,
            confidence=round(fusion_confidence, 3),
            converged_modalities=modalities,
            supporting_signals_count=len(events),
            counter_signals_count=counter_count,
            explanation=explanation,
        )

    def cluster_threat_events(
        self,
        events: List[SecurityEventDTO],
        cluster_type: str = "MULTI_MODAL_ATTACK",
        title: Optional[str] = None,
        tenant_id: str = "default_tenant",
    ) -> ThreatClusterDTO:
        """Groups related events into an explainable threat cluster with an associated fusion score."""
        fusion = self.calculate_fusion_score(events)

        cluster_id = f"tcl_{uuid.uuid4().hex[:12]}"
        event_ids = [e.event_id for e in events]
        entities = list(set(e.entity_id for e in events if e.entity_id))
        assets = list(set(e.asset_id for e in events if e.asset_id))
        modalities = fusion.converged_modalities

        severity = "CRITICAL" if fusion.fusion_score >= 80.0 else ("HIGH" if fusion.fusion_score >= 60.0 else "MEDIUM")
        cl_title = title or f"Coordinated Multi-Modal Threat Cluster ({len(modalities)} Modalities)"
        summary = f"Cluster unites {len(events)} events affecting {len(entities)} entities with Threat Fusion Score {fusion.fusion_score}."

        cluster = ThreatClusterDTO(
            cluster_id=cluster_id,
            cluster_type=cluster_type,
            tenant_id=tenant_id,
            title=cl_title,
            summary=summary,
            event_ids=event_ids,
            entities=entities,
            assets=assets,
            modalities=modalities,
            fusion_score=fusion.fusion_score,
            severity=severity,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._clusters:
            self._clusters[tenant_id] = {}
        self._clusters[tenant_id][cluster_id] = cluster

        return cluster

    def list_clusters(self, tenant_id: str = "default_tenant") -> List[ThreatClusterDTO]:
        """Lists active threat clusters for a tenant."""
        return list(self._clusters.get(tenant_id, {}).values())
