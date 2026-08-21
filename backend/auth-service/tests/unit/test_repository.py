"""Unit tests for Evidence Consolidation Repository Interface (Phase 3.9 Part 1A.25)."""

import pytest
import uuid
from unittest.mock import AsyncMock
from app.repositories.evidence_consolidation_repository import EvidenceConsolidationRepository


@pytest.mark.asyncio
async def test_repository_queries():
    mock_db = AsyncMock()
    mock_res = AsyncMock()
    mock_res.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_res
    repo = EvidenceConsolidationRepository(mock_db)

    scan_id = uuid.uuid4()
    findings = await repo.get_findings_by_scan_id(scan_id)
    evidence = await repo.get_evidence_by_scan_id(scan_id)

    assert findings == []
    assert evidence == []
