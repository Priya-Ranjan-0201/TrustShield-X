"""Unit tests for Async DEX Repository (Phase 3.7 Part 1A.6)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.dex_repository import DEXRepository
from app.schemas.dex_intelligence_models import (
    MultiDEXIntelligenceDTO,
    DEXFileIntelligenceDTO,
    DEXHeaderDTO,
    ClassDTO,
    MethodDTO,
    FieldDTO,
    PackageDTO,
)


@pytest.mark.asyncio
async def test_dex_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = DEXRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = MultiDEXIntelligenceDTO(
        total_dex_files=1,
        total_classes_count=1,
        total_methods_count=1,
        total_fields_count=1,
        dex_files=[
            DEXFileIntelligenceDTO(
                dex_name="classes.dex",
                dex_order=0,
                sha256="a" * 64,
                sha1="b" * 40,
                file_size=500,
                header=DEXHeaderDTO(
                    magic_version="dex\n035\x00",
                    checksum="12345678",
                    checksum_valid=True,
                    sha1_signature="b" * 40,
                    file_size=500,
                    header_size=112,
                    endian_tag="0x12345678",
                ),
                classes=[
                    ClassDTO(
                        name="Lcom/test/Main;",
                        package_name="com.test",
                        superclass="Ljava/lang/Object;",
                        methods=[MethodDTO(name="run", return_type="V")],
                        fields=[FieldDTO(name="id", field_type="I")],
                    )
                ],
            )
        ],
        packages=[PackageDTO(package_name="com.test", class_count=1)],
    )

    models = await repo.save_full_dex_intelligence(scan_id, dto)
    assert len(models) == 1
    assert models[0].scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
