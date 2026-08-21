"""Unit tests for File Descriptor Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DocumentProviderOperationDTO


def test_file_descriptor_dto():
    dop = DocumentProviderOperationDTO(
        caller_method="com.bank.FD.open",
        document_uri="content://com.android.providers.media/123",
        action="OPEN_FILE_DESCRIPTOR",
        has_persistable_permission=True,
    )

    assert dop.action == "OPEN_FILE_DESCRIPTOR"
    assert dop.has_persistable_permission is True
