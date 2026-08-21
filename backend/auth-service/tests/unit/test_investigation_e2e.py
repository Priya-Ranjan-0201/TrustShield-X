import pytest
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService
from app.services.knowledge.security_reasoning_engine import SecurityReasoningEngine
from app.services.knowledge.digital_trust_score_engine import DigitalTrustScoreEngine
from app.services.knowledge.investigation_intelligence_engine import InvestigationIntelligenceEngine
from app.services.knowledge.investigator_copilot_service import InvestigatorCopilotService
from app.schemas.knowledge_fabric_models import CopilotQueryRequestDTO


def test_full_phase_7_investigation_and_reasoning_e2e():
    """
    E2E Integration Test: Digital Trust Knowledge Fabric + Security Reasoning + Investigator Copilot
    Loop: Observe → Detect → Normalize → Correlate → Reason → Investigate → Copilot → Trust Profile
    """
    # 1. Register Knowledge Objects in Fabric
    fabric = KnowledgeFabricService()
    entity_obj = fabric.register_object(
        object_type="ENTITY",
        canonical_reference="secure-verification-hdfc-portal.net",
        tenant_id="tenant_p7_e2e",
        confidence=0.95,
        classification="RESTRICTED",
    )
    evid_obj = fabric.register_object(
        object_type="EVIDENCE",
        canonical_reference="apk_sms_interceptor_dex_hash",
        tenant_id="tenant_p7_e2e",
        confidence=0.98,
    )
    camp_obj = fabric.register_object(
        object_type="CAMPAIGN",
        canonical_reference="CAMP-2026-0891",
        tenant_id="tenant_p7_e2e",
        confidence=0.90,
    )

    # 2. Establish Explicit Relationships
    rel = fabric.link_objects(
        source_id=entity_obj.knowledge_object_id,
        target_id=camp_obj.knowledge_object_id,
        relationship_type="ASSOCIATED_WITH",
        confidence=0.95,
        evidence_ids=[evid_obj.knowledge_object_id],
        tenant_id="tenant_p7_e2e",
    )
    assert rel.relationship_type == "ASSOCIATED_WITH"

    # 3. Capture Point-in-Time Snapshot
    snap = fabric.create_snapshot("Initial Campaign Linkage Snapshot", "tenant_p7_e2e")
    assert snap.object_count == 3

    # 4. Security Reasoning Engine Evaluation
    reasoning = SecurityReasoningEngine(fabric)
    claim_res = reasoning.evaluate_claim(
        question="Is secure-verification-hdfc-portal.net associated with CAMP-2026-0891?",
        target_entity_reference="secure-verification-hdfc-portal.net",
        supporting_evidence_ids=[evid_obj.knowledge_object_id],
        base_confidence=0.95,
        tenant_id="tenant_p7_e2e",
    )
    assert claim_res.reasoning_state in ("VERIFIED", "STRONG_INFERENCE")

    # 5. Digital Trust Score & Profile
    trust_engine = DigitalTrustScoreEngine(fabric)
    profile = trust_engine.get_or_create_profile(entity_obj.canonical_reference, tenant_id="tenant_p7_e2e")
    assert profile.trust_score >= 0.0

    updated_profile = trust_engine.update_trust_profile(
        entity_id=entity_obj.canonical_reference,
        new_trust_score=28.5,
        reason="Verified banking phishing portal association",
        evidence_ids=[evid_obj.knowledge_object_id],
        tenant_id="tenant_p7_e2e",
    )
    assert updated_profile.trust_score == 28.5
    assert len(updated_profile.trust_history) == 2

    # 6. Investigation Workspace & Zero-Hallucination Attack Story
    inv_engine = InvestigationIntelligenceEngine(fabric)
    inv_session = inv_engine.create_investigation(
        title="Banking Phishing Campaign Investigation",
        entity_ids=[entity_obj.knowledge_object_id],
        evidence_ids=[evid_obj.knowledge_object_id],
        campaign_ids=[camp_obj.knowledge_object_id],
        tenant_id="tenant_p7_e2e",
    )
    assert inv_session.status == "ACTIVE"

    recs = inv_engine.recommend_investigation_steps(inv_session.investigation_id, "tenant_p7_e2e")
    assert len(recs) >= 2

    story = inv_engine.generate_attack_story(camp_obj.canonical_reference, [
        {"stage": "INITIAL_OBSERVATION", "description": "Suspicious APK uploaded", "evidence_id": evid_obj.knowledge_object_id}
    ])
    assert len(story.stages) == 7

    # 7. Investigator Copilot Grounded Query
    copilot = InvestigatorCopilotService(fabric, reasoning)
    copilot_req = CopilotQueryRequestDTO(
        query="Why is secure-verification-hdfc-portal.net suspicious?",
        investigation_id=inv_session.investigation_id,
        tenant_id="tenant_p7_e2e",
    )
    copilot_res = copilot.process_query(copilot_req)
    assert copilot_res.confidence >= 0.80
    assert len(copilot_res.citations) >= 1
    assert len(copilot_res.recommended_next_steps) >= 1
