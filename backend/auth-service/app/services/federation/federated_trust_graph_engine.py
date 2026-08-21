"""
TruthShield X — Federated Digital Trust Graph & Attribution Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.federation_models import ActorHypothesisDTO


class FederatedTrustGraphEngine:
    """Maintains federated multi-tenant threat graph connections with cautious attribution hypothesis models."""

    def __init__(self):
        # source_node -> target_node -> edge_data
        self._edges: Dict[str, Dict[str, Dict[str, Any]]] = {}
        # hypothesis_id -> ActorHypothesisDTO
        self._hypotheses: Dict[str, ActorHypothesisDTO] = {}

    def add_federated_edge(
        self,
        source_id: str,
        target_id: str,
        relationship: str = "RELATED_TO",
        confidence: float = 0.85,
        sharing_scope: str = "GLOBAL",
    ) -> Dict[str, Any]:
        """Creates a cautious federated relationship edge in the trust graph."""
        if source_id not in self._edges:
            self._edges[source_id] = {}

        edge = {
            "source": source_id,
            "target": target_id,
            "relationship": relationship,
            "confidence": confidence,
            "sharing_scope": sharing_scope,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._edges[source_id][target_id] = edge
        return edge

    def create_actor_hypothesis(
        self,
        actor_label: str,
        supporting_evidence_ids: List[str],
        counter_evidence_ids: Optional[List[str]] = None,
        alternative_hypotheses: Optional[List[str]] = None,
        confidence: float = 0.70,
    ) -> ActorHypothesisDTO:
        """Constructs an unconfirmed actor hypothesis with explicit counter-evidence and alternative hypotheses."""
        hyp_id = f"hyp_{uuid.uuid4().hex[:10]}"
        hyp = ActorHypothesisDTO(
            hypothesis_id=hyp_id,
            actor_label=actor_label,
            confidence=max(0.1, min(0.95, confidence)),
            supporting_evidence_ids=supporting_evidence_ids,
            counter_evidence_ids=counter_evidence_ids or [],
            alternative_hypotheses=alternative_hypotheses or ["Opportunistic Cybercrime Syndicate", "Adversarial Copycat"],
            status="HYPOTHESIS_UNCONFIRMED",
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        self._hypotheses[hyp_id] = hyp
        return hyp

    def get_related_nodes(self, node_id: str, requesting_scope: str = "GLOBAL") -> List[Dict[str, Any]]:
        """Retrieves edges connected to node enforcing sharing clearance."""
        connected = self._edges.get(node_id, {})
        results = []
        for target, data in connected.items():
            if data["sharing_scope"] == "GLOBAL" or data["sharing_scope"] == requesting_scope:
                results.append(data)
        return results
