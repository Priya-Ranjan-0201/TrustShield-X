"""Unit tests for Certificate Parsing DTOs (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import CryptoCertificateDTO


def test_certificate_dto():
    cert = CryptoCertificateDTO(issuer_dn="CN=Bank CA", subject_dn="CN=api.bank.com", serial_number="123456789", is_pinned=True)

    assert cert.issuer_dn == "CN=Bank CA"
    assert cert.subject_dn == "CN=api.bank.com"
    assert cert.is_pinned is True
