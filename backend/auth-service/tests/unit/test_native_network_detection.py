"""Unit tests for Native Networking Analysis (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEvidenceDTO


def test_native_networking_evidence():
    ev = NetworkEvidenceDTO(
        dex_id="libnative-net.so",
        class_name="JNI",
        method_name="Java_com_bank_NativeBridge_connectSocket",
        instruction_offset=128,
        evidence_type="NATIVE_SOCKET_CALL",
        raw_evidence="connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))",
    )

    assert ev.evidence_type == "NATIVE_SOCKET_CALL"
    assert "connect" in ev.raw_evidence
