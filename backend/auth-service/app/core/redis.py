import time
import redis.asyncio as redis
from app.core.config import settings

# Global redis pool
redis_pool: redis.ConnectionPool | None = None


def get_redis_pool() -> redis.ConnectionPool:
    global redis_pool
    if redis_pool is None:
        redis_pool = redis.ConnectionPool.from_url(
            settings.redis_connection_url,
            decode_responses=True,
            max_connections=20,
        )
    return redis_pool


async def get_redis_client() -> redis.Redis:
    pool = get_redis_pool()
    return redis.Redis(connection_pool=pool)


async def check_rate_limit(
    key: str | None = None,
    limit: int | None = None,
    period_seconds: int | None = None,
    *,
    key_prefix: str | None = None,
    identifier: str | None = None,
    max_attempts: int | None = None,
    window_seconds: int | None = None,
) -> tuple[bool, int]:
    """Check fixed/sliding rate limit using Redis counter. Returns (is_allowed, retry_after_seconds)."""
    full_key = key or f"{key_prefix}:{identifier}"
    max_limit = limit if limit is not None else (max_attempts or 5)
    window = period_seconds if period_seconds is not None else (window_seconds or 900)

    try:
        client = await get_redis_client()
        current_time = int(time.time())
        window_key = f"rate:{full_key}:{current_time // window}"
        
        async with client.pipeline(transaction=True) as pipe:
            pipe.incr(window_key)
            pipe.expire(window_key, window + 5)
            results = await pipe.execute()
            count = results[0]

        if count > max_limit:
            time_passed_in_window = current_time % window
            retry_after = window - time_passed_in_window
            return False, max(retry_after, 1)

        return True, 0
    except Exception:
        # Fallback to allow request if Redis is temporarily unreachable in dev
        return True, 0


async def blacklist_jti(jti: str, expire_seconds: int) -> None:
    """Blacklist a revoked JWT JTI."""
    try:
        client = await get_redis_client()
        await client.setex(f"jwt:blacklist:{jti}", expire_seconds, "1")
    except Exception:
        pass


async def is_jti_blacklisted(jti: str) -> bool:
    """Check if JTI is blacklisted."""
    try:
        client = await get_redis_client()
        result = await client.get(f"jwt:blacklist:{jti}")
        return result is not None
    except Exception:
        return False


async def mark_user_tokens_revoked_in_cache(user_id: str) -> None:
    """Mark all tokens for user revoked until timestamp."""
    try:
        client = await get_redis_client()
        # Store user revocation cutoff timestamp for 7 days
        await client.setex(f"user:revocation:{user_id}", 7 * 86400, str(int(time.time())))
    except Exception:
        pass


async def revoke_user_sessions(user_id: str) -> None:
    """Alias for mark_user_tokens_revoked_in_cache."""
    await mark_user_tokens_revoked_in_cache(user_id)


async def get_user_revocation_cutoff(user_id: str) -> int | None:
    """Get timestamp before which user tokens are invalid."""
    try:
        client = await get_redis_client()
        val = await client.get(f"user:revocation:{user_id}")
        return int(val) if val else None
    except Exception:
        return None
