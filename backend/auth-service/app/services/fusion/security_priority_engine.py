"""
TruthShield X — Security Priority, Blast Radius & Attack Path Analysis Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.fusion_models import (
    BlastRadiusDTO,
    AttackPathDTO,
    AttackPathNodeDTO,
    SecurityEventDTO,
)


class SecurityPriorityEngine:
    """Calculates operational priority rankings, blast radius projections, and constructs multi-stage attack paths."""

    def calculate_priority(
        self,
        event: SecurityEventDTO,
        asset_criticality: str = "MEDIUM",
        campaign_velocity: float = 1.0,
    ) -> Dict[str, Any]:
        """Calculates prioritized score and level for security operations."""
        crit_weights = {"CRITICAL": 1.5, "HIGH": 1.25, "MEDIUM": 1.0, "LOW": 0.8}
        crit_mult = crit_weights.get(asset_criticality.upper(), 1.0)

        raw_score = (
            (event.risk_score * 0.35)
            + (event.exposure_score * 0.25)
            + ((100.0 - event.trust_score) * 0.20)
            + (event.confidence * 20.0)
        )
        final_score = min(100.0, round(raw_score * crit_mult * min(1.3, campaign_velocity), 1))

        if final_score >= 80.0:
            level = "P1_CRITICAL"
        elif final_score >= 60.0:
            level = "P2_HIGH"
        elif final_score >= 40.0:
            level = "P3_MEDIUM"
        else:
            level = "P4_LOW"

        return {
            "priority_score": final_score,
            "priority_level": level,
            "reason": f"Evaluated event severity {event.severity} with criticality {asset_criticality} and campaign velocity {campaign_velocity:.2f}.",
        }

    def analyze_blast_radius(
        self,
        target_identifier: str,
        connected_assets: List[str],
        connected_entities: List[str],
        related_campaigns: List[str],
        affected_services: Optional[List[str]] = None,
    ) -> BlastRadiusDTO:
        """Projects potential blast radius across connected infrastructure."""
        asset_count = len(connected_assets)
        entity_count = len(connected_entities)
        camp_count = len(related_campaigns)

        score = min(100.0, (asset_count * 15.0) + (entity_count * 10.0) + (camp_count * 20.0))
        level = "CRITICAL_BLAST_RADIUS" if score >= 75.0 else ("HIGH_BLAST_RADIUS" if score >= 50.0 else "MODERATE_BLAST_RADIUS")

        rationale = (
            f"Target '{target_identifier}' links to {asset_count} asset(s), {entity_count} entity(ies), "
            f"and {camp_count} active campaign(s). Blast radius calculated at {score:.1f} pts."
        )

        return BlastRadiusDTO(
            target_entity_or_asset=target_identifier,
            blast_radius_score=round(score, 1),
            affected_assets=connected_assets,
            connected_entities=connected_entities,
            related_campaigns=related_campaigns,
            affected_services=affected_services or ["AuthenticationGateway", "PublicAPIRouter"],
            impact_level="POTENTIAL_IMPACT",
            rationale=rationale,
        )

    def construct_attack_path(
        self,
        entry_point: str,
        target_asset: str,
        campaign_name: str,
        intermediate_infra: Optional[List[str]] = None,
    ) -> AttackPathDTO:
        """Constructs an attack path clearly qualifying observed vs potential vs inferred nodes."""
        path_id = f"path_{uuid.uuid4().hex[:12]}"
        nodes: List[AttackPathNodeDTO] = []

        # 1. Entry point (Observed)
        nodes.append(AttackPathNodeDTO(
            node_id="node_entry",
            node_type="ENTRY",
            label=f"Phishing Delivery / Entry ({entry_point})",
            status="OBSERVED_PATH",
            confidence=0.96,
        ))

        # 2. Intermediate infrastructure
        if intermediate_infra:
            for i, infra in enumerate(intermediate_infra):
                nodes.append(AttackPathNodeDTO(
                    node_id=f"node_infra_{i}",
                    node_type="INFRASTRUCTURE",
                    label=f"Staging / C2 Infrastructure ({infra})",
                    status="OBSERVED_PATH",
                    confidence=0.92,
                ))

        # 3. Campaign (Inferred / Correlated)
        nodes.append(AttackPathNodeDTO(
            node_id="node_camp",
            node_type="CAMPAIGN",
            label=f"Campaign Linkage ({campaign_name})",
            status="INFERRED_PATH",
            confidence=0.88,
        ))

        # 4. Target Asset (Potential Impact)
        nodes.append(AttackPathNodeDTO(
            node_id="node_target",
            node_type="TARGET",
            label=f"Target Enterprise Asset ({target_asset})",
            status="POTENTIAL_PATH",
            confidence=0.75,
        ))

        return AttackPathDTO(
            path_id=path_id,
            target_asset=target_asset,
            path_nodes=nodes,
            overall_confidence=0.87,
            constructed_at=datetime.now(timezone.utc).isoformat(),
        )
