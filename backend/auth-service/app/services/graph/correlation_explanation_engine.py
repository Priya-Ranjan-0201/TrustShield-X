"""Correlation Explanation Engine (Phase 4.0 Part 5 — Sections 18, 69-70).

Generates evidence-grounded, human-readable explanations answering:
1. What is connected?
2. Why are they connected?
3. What evidence supports it?
4. How strong is the relationship?
5. What could make it incorrect (false correlation risks)?
6. What remains unresolved?
"""

from typing import Optional
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    CorrelationExplanationDTO,
)


class CorrelationExplanationEngine:
    """Produces structured explanations for graph relationships."""

    @classmethod
    def explain(
        cls,
        rel: GraphRelationshipDTO,
        source_ent: Optional[CanonicalEntityDTO] = None,
        target_ent: Optional[CanonicalEntityDTO] = None,
    ) -> CorrelationExplanationDTO:
        src_label = source_ent.display_value if source_ent else rel.source_entity_id
        tgt_label = target_ent.display_value if target_ent else rel.target_entity_id

        # 1. Why connected
        why = f"Entities {src_label} and {tgt_label} are linked by {rel.relationship_type} via method {rel.correlation_method}."
        if rel.relationship_type == "USES_CERTIFICATE":
            why = f"Application or host {src_label} is cryptographically signed by certificate fingerprint {tgt_label}."
        elif rel.relationship_type == "HOSTS":
            why = f"Domain {tgt_label} acts as the hosting network authority for resource {src_label}."
        elif rel.relationship_type == "COLLECTS":
            why = f"Resource {src_label} was observed extracting or soliciting payment identifier {tgt_label}."
        elif rel.relationship_type == "MATCHES":
            why = f"Entity {src_label} matches verified indicator or hash {tgt_label}."

        # 2. False correlation risk
        false_risk = "Low risk of coincidence due to cryptographic or exact identifier matching."
        if rel.relationship_type == "SHARES_INFRASTRUCTURE" or rel.correlation_method == "TEMPORAL_ANALYZER":
            false_risk = "Potential false correlation if resources share multi-tenant CDN/cloud infrastructure or temporal coincidence."
        elif "cloudflare" in src_label.lower() or "cloudflare" in tgt_label.lower() or "aws" in src_label.lower():
            false_risk = "High probability of shared public CDN or cloud hosting provider rather than dedicated adversary infrastructure."

        # 3. Unresolved questions
        unresolved = []
        if rel.confidence in ["LOW", "VERY_LOW", "UNKNOWN"]:
            unresolved.append("Requires additional corroborating evidence from independent network or binary analyses.")
        if rel.status == "CONFLICTED":
            unresolved.append("Conflicting threat feeds or observations detected; requires manual analyst verification.")

        signals = [
            f"Relationship Type: {rel.relationship_type}",
            f"Correlation Method: {rel.correlation_method}",
            f"Evidence Strength: {rel.evidence_strength}",
            f"Source Count: {rel.source_count}",
        ]

        return CorrelationExplanationDTO(
            relationship_id=rel.relationship_id,
            source_entity=src_label,
            target_entity=tgt_label,
            relationship_type=rel.relationship_type,
            confidence=rel.confidence,
            why_connected=why,
            evidence_signals=signals,
            correlation_rule=rel.correlation_method,
            rule_version=rel.correlation_version,
            false_correlation_risk=false_risk,
            unresolved_questions=unresolved,
        )
