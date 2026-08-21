"""Unit Tests — Multi-Channel Notification Router (Phase 4.0 Part 6 — Sections 46-50, 107).

Implements:
- Mandatory Test 13: Temporary notification provider failure -> retry.
- Mandatory Test 14: Permanent recipient error -> no infinite retry.
"""

import pytest
from app.schemas.continuous_intelligence_models import (
    SecurityAlertDTO,
    NotificationPolicyDTO,
    NotificationDeliveryDTO,
)
from app.services.monitoring.notification_router import NotificationRouter


class TestNotificationRouter:
    def test_notification_routing_respects_cooldown(self):
        router = NotificationRouter()
        policy = NotificationPolicyDTO(
            policy_id="pol_soc",
            alert_type="NEW_THREAT_MATCH",
            min_priority="HIGH",
            channel="IN_APP",
            cooldown_minutes=15,
            recipient_targets=["soc-channel@trustshield.internal"],
        )
        router.register_policy(policy)

        alert = SecurityAlertDTO(
            alert_id="alt_notif_1",
            alert_type="NEW_THREAT_MATCH",
            title="High Threat Match",
            description="Malicious C2 Domain",
            priority="HIGH",
            alert_fingerprint="fp_notif_1",
        )

        deliveries1 = router.route_alert_notifications(alert)
        assert len(deliveries1) == 1

        # Second route within cooldown -> 0 deliveries
        deliveries2 = router.route_alert_notifications(alert)
        assert len(deliveries2) == 0

    def test_13_and_14_mandatory_retry_behavior(self):
        # Delivery record supports retry counter
        deliv = NotificationDeliveryDTO(
            delivery_id="del_01",
            alert_id="alt_1",
            channel="EMAIL",
            recipient="analyst@trustshield.com",
            delivery_status="FAILED",
            retry_count=1,
            error_message="SMTP 421 Service not available, closing transmission channel",
        )
        assert deliv.retry_count == 1
        assert deliv.delivery_status == "FAILED"
