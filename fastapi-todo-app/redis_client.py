from typing import Optional

try:
    import redis.asyncio as aioredis
except Exception:  # pragma: no cover - optional runtime dependency
    aioredis = None  # type: ignore

_redis: Optional[object] = None


async def connect_redis(url: str = "redis://redis:6379/0"):
    """Create and return a global redis client (async).

    If the `redis` package is not installed this becomes a no-op and
    functions return None so local imports/tests don't fail.
    """
    global _redis
    if aioredis is None:
        return None
    if _redis is None:
        _redis = aioredis.from_url(url, encoding="utf-8", decode_responses=True)
    return _redis


def get_redis():
    """Return the connected redis client or None."""
    return _redis


async def close_redis():
    global _redis
    if aioredis is None or _redis is None:
        return None
    try:
        await _redis.close()
        await _redis.connection_pool.disconnect()
    finally:
        _redis = None
