import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan_result import ScanResult


class ResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_result(
        self,
        scan_id: uuid.UUID,
        trust_score: int,
        risk_score: int,
        confidence_score: float,
        findings_json: dict,
        execution_time_ms: int = 0,
        module_id: uuid.UUID | None = None,
    ) -> ScanResult:
        result = ScanResult(
            scan_id=scan_id,
            module_id=module_id,
            trust_score=trust_score,
            risk_score=risk_score,
            confidence_score=confidence_score,
            findings_json=findings_json,
            execution_time_ms=execution_time_ms,
        )
        self.session.add(result)
        await self.session.commit()
        return result

    async def get_by_scan_id(self, scan_id: uuid.UUID) -> ScanResult | None:
        stmt = select(ScanResult).where(ScanResult.scan_id == scan_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
