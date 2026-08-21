import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan_event import ScanEvent


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_event(
        self,
        scan_id: uuid.UUID,
        event_type: str,
        description: str,
        event_data_json: dict | None = None,
    ) -> ScanEvent:
        event = ScanEvent(
            scan_id=scan_id,
            event_type=event_type,
            description=description,
            event_data_json=event_data_json or {},
        )
        self.session.add(event)
        await self.session.commit()
        return event

    async def get_scan_events(self, scan_id: uuid.UUID) -> list[ScanEvent]:
        stmt = (
            select(ScanEvent)
            .where(ScanEvent.scan_id == scan_id)
            .order_by(ScanEvent.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
