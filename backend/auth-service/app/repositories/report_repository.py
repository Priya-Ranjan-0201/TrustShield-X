import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_reports(
        self, user_id: uuid.UUID, limit: int = 50, offset: int = 0
    ) -> list[Report]:
        stmt = (
            select(Report)
            .where(Report.user_id == user_id)
            .order_by(Report.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
