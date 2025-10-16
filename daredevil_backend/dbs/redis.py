from redis.asyncio import Redis

from configs import get_settings

settings = get_settings()


_token_list = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
)


# jwt id
async def add_jti_to_list(jti: str):
    await _token_list.set(jti, "listed")


# jwt id
async def is_jti_listed(jti: str) -> bool:
    return await _token_list.exists(jti)
