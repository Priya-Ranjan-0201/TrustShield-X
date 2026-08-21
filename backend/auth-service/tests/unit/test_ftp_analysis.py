"""Unit tests for FTP / SFTP File Transfer Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkFileTransferDTO


def test_file_transfer_dto():
    ft = NetworkFileTransferDTO(
        caller_method="com.bank.SFTP.upload",
        protocol="SFTP",
        host="sftp.bank.com",
        port=22,
    )

    assert ft.protocol == "SFTP"
    assert ft.port == 22
