"""Unit tests for Evidence Consolidation Repository Persistence (Phase 3.9 Part 1A.25)."""

import pytest
import uuid
from unittest.mock import AsyncMock
from app.repositories.evidence_consolidation_repository import EvidenceConsolidationRepository
from app.schemas.evidence_consolidation_models import ConsolidationResultDTO, CanonicalFindingDTO


@pytest.mark.asyncio
async def test_evidence_repository_save():
    mock_db = AsyncMock()
    repo = EvidenceConsolidationRepository(mock_db)

    dto = ConsolidationResultDTO(
        findings=[
            CanonicalFindingDTO(
                finding_id="f1",
                finding_type="NETWORK_ENDPOINT_OBSERVED",
                finding_category="NETWORK",
                title="Title",
                description="Desc",
            )
        ]
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_consolidation_result(scan_id, dto)

    assert model.finding_id == "f1"
    assert mock_db.commit.called
