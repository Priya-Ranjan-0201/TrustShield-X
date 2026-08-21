from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.repositories.scan_repository import ScanRepository
from app.repositories.notification_repository import NotificationRepository
from app.schemas.envelope import ResponseEnvelope, ResponseMeta

router = APIRouter()


@router.get("/stats", response_model=ResponseEnvelope[dict])
async def get_dashboard_stats(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scan_repo = ScanRepository(db)
    notif_repo = NotificationRepository(db)

    total_scans = await scan_repo.get_user_scan_count(current_user.id)
    dangerous_count = await scan_repo.get_user_dangerous_count(current_user.id)
    user_notifications = await notif_repo.get_user_notifications(current_user.id, limit=50)
    unread_alerts = sum(1 for n in user_notifications if not n.read)

    trust_score = 94 if total_scans == 0 else max(10, 100 - (dangerous_count * 15))
    trust_status = "TRUSTED" if trust_score >= 90 else "MEDIUM RISK" if trust_score >= 50 else "DANGEROUS"

    return ResponseEnvelope[dict](
        success=True,
        message="Dashboard statistics retrieved.",
        data={
          "trustScore": trust_score,
          "trustStatus": trust_status,
          "totalScans": total_scans,
          "threatsBlocked": dangerous_count,
          "activeAlerts": unread_alerts,
        },
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )


@router.get("/recent-activity", response_model=ResponseEnvelope[list[dict]])
async def get_recent_activity(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    scan_repo = ScanRepository(db)
    scans = await scan_repo.get_user_scans(current_user.id, limit=10)

    results = [
        {
            "id": str(scan.id),
            "target": scan.target,
            "scan_type": scan.scan_type,
            "trust_score": scan.trust_score or 0,
            "status": scan.status,
            "scanned_at": scan.scanned_at.isoformat(),
            "summary": scan.summary or "Inspection record created.",
        }
        for scan in scans
    ]

    return ResponseEnvelope[list[dict]](
        success=True,
        message="Recent activity retrieved.",
        data=results,
        meta=ResponseMeta(
            traceId=getattr(request.state, "trace_id", "trace-id-default"),
            version="v1",
        ),
    )
