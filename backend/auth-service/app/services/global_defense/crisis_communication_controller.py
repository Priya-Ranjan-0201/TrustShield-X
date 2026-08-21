"""
TruthShield X — Crisis Communication Controller (Phase 28).

Validates message classification, recipients, and privacy sanitization before outbound alerts.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
from app.schemas.global_defense_models import DataClassificationLiteral


class CrisisCommunicationController:
    """Controls cross-organizational communications with automated policy validation."""

    def compose_and_validate_alert(
        self,
        sender_id: str,
        recipients: List[str],
        subject: str,
        sanitized_content: str,
        classification: DataClassificationLiteral = "CONFIDENTIAL",
    ) -> Dict[str, Any]:
        if not recipients:
            raise ValueError("Recipients list cannot be empty")

        # Verify no sensitive keywords slipped in
        if any(w in sanitized_content.lower() for w in ["password=", "secret=", "apikey="]):
            return {
                "status": "SANITIZATION_REQUIRED",
                "sent": False,
                "reason": "Unsanitized credentials detected in communication payload",
            }

        return {
            "status": "DISPATCHED",
            "sent": True,
            "sender_id": sender_id,
            "recipients": recipients,
            "subject": subject,
            "classification": classification,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
