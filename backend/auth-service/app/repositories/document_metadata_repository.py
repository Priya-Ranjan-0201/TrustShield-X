import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_metadata import DocumentMetadata


class DocumentMetadataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_metadata(
        self,
        scan_id: uuid.UUID,
        document_type: str,
        extracted_fields: dict,
        ocr_confidence: float | None = None,
        image_quality_metrics: dict | None = None,
    ) -> DocumentMetadata:
        metadata = DocumentMetadata(
            scan_id=scan_id,
            document_type=document_type,
            extracted_fields=extracted_fields,
            ocr_confidence=ocr_confidence,
            image_quality_metrics=image_quality_metrics,
        )
        self.session.add(metadata)
        await self.session.commit()
        return metadata

    async def get_by_scan_id(self, scan_id: uuid.UUID) -> DocumentMetadata | None:
        stmt = select(DocumentMetadata).where(DocumentMetadata.scan_id == scan_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
