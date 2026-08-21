"""Unit tests for NFC Hardware Communication (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkNfcDTO


def test_nfc_dto():
    nfc = NetworkNfcDTO(
        caller_method="com.bank.NFC.readCard",
        technology="NDEF",
        action="READ",
    )

    assert nfc.technology == "NDEF"
    assert nfc.action == "READ"
