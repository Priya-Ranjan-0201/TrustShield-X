"""Attack Chain Reconstruction Engine (Phase 4.0 Part 5 — Sections 28-31, 93).

Reconstructs evidence-supported attack chains with explicit stage progression
(ENTRY_POINT -> EXECUTION -> COLLECTION -> TRANSMISSION -> IMPACT) and strict
safeguards against fabricating unobserved or speculative steps.
"""

from typing import List, Dict, Optional
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    AttackChainDTO,
    AttackChainStepDTO,
)


class AttackChainEngine:
    """Reconstructs evidence-supported attack chains without speculative fabrication."""

    @classmethod
    def reconstruct_chains(
        cls,
        entities: List[CanonicalEntityDTO],
        relationships: List[GraphRelationshipDTO],
        case_id: Optional[str] = None,
    ) -> List[AttackChainDTO]:
        chains: List[AttackChainDTO] = []
        entity_map = {e.entity_id: e for e in entities}

        # 1. Phishing to Payment Fraud Attack Chain
        phish_urls = [e for e in entities if e.entity_type in ["URL", "PHISHING_KIT"]]
        payment_ids = [e for e in entities if e.entity_type in ["UPI_ID", "BANK_IDENTIFIER"]]

        for phish in phish_urls:
            steps: List[AttackChainStepDTO] = []
            
            # Step 1: Entry Point (Confirmed)
            steps.append(
                AttackChainStepDTO(
                    step_id=f"step_{phish.entity_id}_1",
                    chain_id="",
                    step_number=1,
                    stage="ENTRY_POINT",
                    title="Phishing URL Distribution",
                    description=f"User lured to malicious endpoint {phish.display_value}",
                    step_state="CONFIRMED_STEP",
                    confidence=phish.confidence,
                    entity_ids=[phish.entity_id],
                )
            )

            # Check if payment identifier is linked
            has_payment = False
            for pay in payment_ids:
                # Check if there is an active relationship
                linked = any(
                    (r.source_entity_id == phish.entity_id and r.target_entity_id == pay.entity_id)
                    or (r.source_entity_id == pay.entity_id and r.target_entity_id == phish.entity_id)
                    for r in relationships
                )
                if linked:
                    has_payment = True
                    # Step 2: Credential & Financial Solicitation
                    steps.append(
                        AttackChainStepDTO(
                            step_id=f"step_{phish.entity_id}_2",
                            chain_id="",
                            step_number=2,
                            stage="COLLECTION",
                            title="Payment Identifier Solicitation",
                            description=f"Phishing page solicits payment to destination {pay.display_value}",
                            step_state="CONFIRMED_STEP",
                            confidence=pay.confidence,
                            entity_ids=[pay.entity_id],
                        )
                    )
                    # Step 3: Financial Impact
                    steps.append(
                        AttackChainStepDTO(
                            step_id=f"step_{phish.entity_id}_3",
                            chain_id="",
                            step_number=3,
                            stage="IMPACT",
                            title="Unauthorized Financial Extraction",
                            description="Direct financial transfer to fraudulent account",
                            step_state="SUPPORTED_STEP",
                            confidence="HIGH",
                            entity_ids=[pay.entity_id],
                        )
                    )
                    break

            if not has_payment:
                # Phishing URL ONLY — DO NOT fabricate credential theft or payment fraud (Section 93 Test 16)
                steps.append(
                    AttackChainStepDTO(
                        step_id=f"step_{phish.entity_id}_2",
                        chain_id="",
                        step_number=2,
                        stage="COLLECTION",
                        title="Credential / Data Collection",
                        description="Potential credential capture page (unverified backend exfiltration)",
                        step_state="POSSIBLE_STEP",
                        confidence="LOW",
                        missing_evidence_note="No concrete post-submission dataflow or payment capture observed.",
                    )
                )

            chain_id = f"chain_phish_{phish.entity_id[-8:]}"
            for s in steps:
                s = s.model_copy(update={"chain_id": chain_id})

            chains.append(
                AttackChainDTO(
                    chain_id=chain_id,
                    case_id=case_id,
                    title=f"Phishing Scam Campaign ({phish.display_value[:40]})",
                    entry_point=phish.display_value,
                    confidence="HIGH" if has_payment else "MEDIUM",
                    status="ACTIVE",
                    steps=steps,
                    missing_steps_count=1 if not has_payment else 0,
                    uncertainty_summary="Post-landing user actions partially observed." if not has_payment else "",
                )
            )

        # 2. APK Malicious Behavior Chain
        packages = [e for e in entities if e.entity_type in ["PACKAGE", "APPLICATION"]]
        for pkg in packages:
            # Check permissions vs network sinks
            has_net_sink = any(
                r.source_entity_id == pkg.entity_id and r.relationship_type in ["COMMUNICATES_WITH", "HOSTS", "EXFILTRATES_TO"]
                for r in relationships
            )

            apk_steps = [
                AttackChainStepDTO(
                    step_id=f"step_{pkg.entity_id}_1",
                    chain_id="",
                    step_number=1,
                    stage="ENTRY_POINT",
                    title="Application Installation",
                    description=f"Package {pkg.display_value} installed on device",
                    step_state="CONFIRMED_STEP",
                    confidence="VERY_HIGH",
                    entity_ids=[pkg.entity_id],
                ),
                AttackChainStepDTO(
                    step_id=f"step_{pkg.entity_id}_2",
                    chain_id="",
                    step_number=2,
                    stage="EXECUTION",
                    title="Permission Acquisition",
                    description="Application requests sensitive runtime permissions",
                    step_state="CONFIRMED_STEP",
                    confidence="HIGH",
                    entity_ids=[pkg.entity_id],
                )
            ]

            if has_net_sink:
                apk_steps.append(
                    AttackChainStepDTO(
                        step_id=f"step_{pkg.entity_id}_3",
                        chain_id="",
                        step_number=3,
                        stage="TRANSMISSION",
                        title="Command & Control Communication",
                        description="Application initiates outbound transmission to external endpoint",
                        step_state="CONFIRMED_STEP",
                        confidence="HIGH",
                    )
                )
            else:
                # Permission WITHOUT network sink -> DO NOT fabricate exfiltration (Section 93 Test 17)
                apk_steps.append(
                    AttackChainStepDTO(
                        step_id=f"step_{pkg.entity_id}_3",
                        chain_id="",
                        step_number=3,
                        stage="TRANSMISSION",
                        title="Remote Exfiltration",
                        description="No active network sink or data exfiltration observed",
                        step_state="MISSING_STEP",
                        confidence="VERY_LOW",
                        missing_evidence_note="No network connection observed in static or behavioral analysis.",
                    )
                )

            apk_chain_id = f"chain_apk_{pkg.entity_id[-8:]}"
            chains.append(
                AttackChainDTO(
                    chain_id=apk_chain_id,
                    case_id=case_id,
                    title=f"Mobile Application Execution Path ({pkg.display_value})",
                    entry_point=pkg.display_value,
                    confidence="HIGH" if has_net_sink else "LOW",
                    status="ACTIVE",
                    steps=apk_steps,
                    missing_steps_count=0 if has_net_sink else 1,
                    uncertainty_summary="No outbound data transmission verified." if not has_net_sink else "",
                )
            )

        return chains
