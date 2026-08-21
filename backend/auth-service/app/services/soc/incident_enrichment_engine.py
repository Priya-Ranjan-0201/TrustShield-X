"""Incident Enrichment Engine (Phase 4.0 Part 7 — Sections 20-21).

Enriches security incidents with authoritative graph relationships, threat campaigns,
attack chains, evidence, and historical observations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.soc_operations_models import SecurityIncidentDTO, SOCAlertDTO


class IncidentEnrichmentEngine:
    """Enriches incidents with contextual security graph data and threat intelligence."""

    @staticmethod
    def enrich_incident(
        incident: SecurityIncidentDTO,
        alerts: List[SOCAlertDTO],
        graph_entities: Optional[List[Dict[str, Any]]] = None,
        campaign: Optional[Dict[str, Any]] = None,
        attack_chain: Optional[Dict[str, Any]] = None,
    ) -> SecurityIncidentDTO:
        # Collect entity IDs
        ents = set([e for a in alerts for e in a.entity_ids])
        if graph_entities:
            for g in graph_entities:
                if "entity_id" in g:
                    ents.add(g["entity_id"])
        incident.entity_count = len(ents)

        # Collect finding and evidence IDs
        findings = set([f for a in alerts for f in a.finding_ids])
        evidence = set([ev for a in alerts for ev in a.evidence_ids])
        incident.finding_count = len(findings)
        incident.evidence_count = len(evidence)

        if campaign and "campaign_id" in campaign:
            incident.campaign_id = campaign["campaign_id"]
        if attack_chain and "chain_id" in attack_chain:
            incident.attack_chain_id = attack_chain["chain_id"]

        incident.updated_at = datetime.now(timezone.utc).isoformat()
        return incident
