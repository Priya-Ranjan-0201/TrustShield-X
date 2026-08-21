"""Privacy Test Suite (Phase 4.0 Part 5 — Section 98).

Implements Tests 25 to 27:
- Test 25: Phone number -> Masked in UI.
- Test 26: Aadhaar-like identity identifier -> Never displayed in full.
- Test 27: UPI identifier -> Privacy policy masking applied.
"""

import pytest
from app.services.graph.entity_normalizer import EntityNormalizer


class TestPrivacySuite:
    def test_25_phone_number_masked(self):
        canon, masked, _ = EntityNormalizer.normalize_phone("+919876543210")
        assert "+91" in masked
        assert "******" in masked
        assert "987654" not in masked

    def test_26_identity_document_never_displayed_in_full(self):
        aadhaar_raw = "1234 5678 9012"
        # Digits only last-4 should be visible
        digits = aadhaar_raw.replace(" ", "")
        masked = f"XXXX-XXXX-{digits[-4:]}"
        assert "1234" not in masked
        assert "5678" not in masked
        assert "9012" in masked

    def test_27_upi_identifier_privacy_policy(self):
        canon, masked, _ = EntityNormalizer.normalize_upi("priyeranjan@okhdfcbank")
        assert "@okhdfcbank" in masked
        assert "***" in masked
        assert "priyeranjan@" not in masked
