from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.schemas.envelope import StandardResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=StandardResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Health check verifying DB and Redis connectivity",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "healthy"
    redis_status = "healthy"

    # Check Database Connectivity
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Check Redis Connectivity
    try:
        redis_client = await get_redis_client()
        await redis_client.ping()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"

    is_healthy = ("unhealthy" not in db_status) and ("unhealthy" not in redis_status)
    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    return StandardResponse(
        success=is_healthy,
        message="Health status evaluated." if is_healthy else "Service health degraded.",
        data={
            "database": db_status,
            "redis": redis_status,
            "overall_status": "UP" if is_healthy else "DOWN",
        },
    )
