"""Unit Tests — Manual Analyst Correlations & Review Queue (Phase 4.0 Part 5 — Sections 79-82)."""

import pytest
from app.schemas.intelligence_graph_models import (
    ManualCorrelationCreateDTO,
    RelationshipReviewActionDTO,
    CorrelationReviewItemDTO,
    GraphRelationshipDTO,
)


class TestManualCorrelationsAndReviewQueue:
    def test_manual_correlation_dto_creation(self):
        dto = ManualCorrelationCreateDTO(
            source_entity_id="e_apk_101",
            target_entity_id="e_c2_domain",
            relationship_type="COMMUNICATES_WITH",
            confidence="HIGH",
            reason="Observed hardcoded string decryption in native library libcore.so",
            evidence_ids=["ev_101", "ev_102"],
        )
        assert dto.source_entity_id == "e_apk_101"
        assert dto.confidence == "HIGH"
        assert len(dto.evidence_ids) == 2

    def test_review_queue_item_prioritization(self):
        item = CorrelationReviewItemDTO(
            review_id="rev_01",
            relationship_id="rel_01",
            source_entity_value="phishing-site.in",
            target_entity_value="fraud@ybl",
            relationship_type="COLLECTS",
            confidence="MEDIUM",
            flag_reason="POTENTIAL_FALSE_POSITIVE",
            priority="HIGH",
            status="PENDING",
        )
        assert item.priority == "HIGH"
        assert item.status == "PENDING"
        assert item.flag_reason == "POTENTIAL_FALSE_POSITIVE"

    def test_relationship_review_actions(self):
        action_confirm = RelationshipReviewActionDTO(action="CONFIRM", reviewer_note="Verified with Wireshark PCAP")
        action_reject = RelationshipReviewActionDTO(action="REJECT", reviewer_note="Shared public CDN only")
        assert action_confirm.action == "CONFIRM"
        assert action_reject.action == "REJECT"
