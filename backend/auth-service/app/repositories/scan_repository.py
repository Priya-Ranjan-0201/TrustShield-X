import uuid
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan_history import ScanHistory
from app.core.scan_lifecycle import ScanStatus, validate_status_transition


class ScanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_scan_record(
        self,
        user_id: uuid.UUID,
        target: str,
        scan_type: str,
        trust_score: int | None = None,
        risk_score: int | None = None,
        confidence_score: float | None = None,
        status: str = "UPLOADED",
        summary: str | None = None,
        file_path: str | None = None,
        file_size_bytes: int | None = None,
        sha256_checksum: str | None = None,
        mime_type: str | None = None,
        module_used: str | None = None,
    ) -> ScanHistory:
        scan = ScanHistory(
            user_id=user_id,
            target=target,
            scan_type=scan_type,
            trust_score=trust_score,
            risk_score=risk_score,
            confidence_score=confidence_score,
            status=status,
            summary=summary,
            file_path=file_path,
            file_size_bytes=file_size_bytes,
            sha256_checksum=sha256_checksum,
            mime_type=mime_type,
            module_used=module_used,
        )
        self.session.add(scan)
        await self.session.commit()
        return scan

    async def update_status(
        self,
        scan_id: uuid.UUID,
        new_status: str,
        summary: str | None = None,
        processing_time_ms: int | None = None,
    ) -> ScanHistory | None:
        stmt = select(ScanHistory).where(ScanHistory.id == scan_id)
        result = await self.session.execute(stmt)
        scan = result.scalar_one_or_none()

        if scan:
            validate_status_transition(scan.status, new_status)
            scan.status = new_status
            if summary:
                scan.summary = summary
            if processing_time_ms is not None:
                scan.processing_time_ms = processing_time_ms
            await self.session.commit()
            return scan
        return None

    async def get_user_scans(
        self,
        user_id: uuid.UUID,
        scan_type: str | None = None,
        search_query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[ScanHistory]:
        stmt = select(ScanHistory).where(ScanHistory.user_id == user_id)

        if scan_type and scan_type != "ALL":
            stmt = stmt.where(ScanHistory.scan_type == scan_type)

        if search_query:
            stmt = stmt.where(ScanHistory.target.ilike(f"%{search_query}%"))

        stmt = stmt.order_by(ScanHistory.scanned_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_scan_count(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count(ScanHistory.id)).where(ScanHistory.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0

    async def get_user_dangerous_count(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count(ScanHistory.id)).where(
            ScanHistory.user_id == user_id, ScanHistory.status == "DANGEROUS"
        )
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0
