"""Unit tests for DocumentsProvider & SAF Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DocumentProviderOperationDTO


def test_documents_provider_dto():
    dop = DocumentProviderOperationDTO(
        caller_method="com.bank.SAF.openDoc",
        document_uri="content://com.android.externalstorage.documents/document/primary%3ADownload",
        action="ACTION_OPEN_DOCUMENT",
        has_persistable_permission=True,
    )

    assert dop.action == "ACTION_OPEN_DOCUMENT"
