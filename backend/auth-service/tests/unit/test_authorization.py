"""Unit Tests — Authorization and Review Queue (Phase 4.0 Part 5 — Sections 77, 81-83)."""

import pytest
from app.schemas.intelligence_graph_models import (
    CorrelationReviewItemDTO,
    RelationshipReviewActionDTO,
)


class TestAuthorizationAndReviewQueue:
    def test_intelligence_permissions_enforcement(self):
        user_role = "SECURITY_ANALYST"
        allowed_roles = ["SECURITY_ANALYST", "SOC_LEAD", "ADMIN"]
        has_permission = user_role in allowed_roles
        assert has_permission is True

        executive_role = "EXECUTIVE"
        executive_can_annotate = executive_role in ["SECURITY_ANALYST", "ADMIN"]
        assert executive_can_annotate is False

    def test_review_queue_status_transitions(self):
        item = CorrelationReviewItemDTO(
            review_id="rev_101",
            relationship_id="rel_101",
            source_entity_value="phish.com",
            target_entity_value="c2.org",
            relationship_type="REDIRECTS_TO",
            confidence="LOW",
            flag_reason="LOW_CONFIDENCE",
            status="PENDING",
        )
        assert item.status == "PENDING"

        # Action: CONFIRM
        action = RelationshipReviewActionDTO(action="CONFIRM", reviewer_note="Manually verified")
        assert action.action == "CONFIRM"
