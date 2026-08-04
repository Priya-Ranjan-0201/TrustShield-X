import uuid
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditLog


class AuditRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_action(
        self,
        action: str,
        ip_address: str,
        trace_id: str,
        user_id: uuid.UUID | None = None,
        user_agent: str | None = None,
        success: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            trace_id=trace_id,
            log_metadata=metadata,
        )
        self.session.add(audit_entry)
        await self.session.commit()
        return audit_entry
