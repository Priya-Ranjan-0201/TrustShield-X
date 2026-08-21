"""Unit Tests — Entity Normalization (Phase 4.0 Part 5 — Sections 4-6, 90)."""

import pytest
from app.services.graph.entity_normalizer import EntityNormalizer


class TestEntityNormalization:
    def test_normalize_domain_punycode_and_trailing_dots(self):
        dom_a, disp_a, hash_a = EntityNormalizer.normalize_domain("HTTP://Example.COM/path/test")
        dom_b, disp_b, hash_b = EntityNormalizer.normalize_domain("https://example.com.")
        assert dom_a == "example.com"
        assert dom_b == "example.com"
        assert hash_a == hash_b

    def test_normalize_url_deterministic_query(self):
        url_a, _, hash_a = EntityNormalizer.normalize_url("https://example.com/login?b=2&a=1")
        url_b, _, hash_b = EntityNormalizer.normalize_url("https://example.com/login?a=1&b=2")
        assert url_a == "https://example.com/login?a=1&b=2"
        assert url_a == url_b
        assert hash_a == hash_b

    def test_normalize_ip_canonical(self):
        ip_v4, _, _ = EntityNormalizer.normalize_ip("192.168.1.1")
        ip_v6, _, _ = EntityNormalizer.normalize_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        assert ip_v4 == "192.168.1.1"
        assert ip_v6 == "2001:db8:85a3::8a2e:370:7334"

    def test_normalize_hash_and_certificate(self):
        h, _, _ = EntityNormalizer.normalize_hash("  a1B2c3d4E5f67890a1B2c3d4E5f67890  ")
        assert h == "a1b2c3d4e5f67890a1b2c3d4e5f67890"

        cert, disp_cert, _ = EntityNormalizer.normalize_certificate("aa:bb:cc:dd")
        assert cert == "AABBCCDD"
        assert disp_cert == "AA:BB:CC:DD"

    def test_normalize_phone_and_privacy_masking(self):
        canon, masked, _ = EntityNormalizer.normalize_phone("+919876543210")
        assert canon == "+919876543210"
        assert masked == "+91******3210"

    def test_normalize_upi_and_privacy_masking(self):
        canon, masked, _ = EntityNormalizer.normalize_upi("merchant_fraud_user@okhdfcbank")
        assert canon == "merchant_fraud_user@okhdfcbank"
        assert "me***er@okhdfcbank" == masked
