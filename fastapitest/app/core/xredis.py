from redis import asyncio as aioredis
from datetime import datetime, timedelta

from redis import Redis

redis: Redis = None


async def init_redis(redis_url):
    global redis
    redis = await aioredis.from_url(redis_url)
    print(f"redis = {redis}")


async def get_redis():
    global redis
    if redis is None:
        await init_redis()
    return redis


async def close_redis():
    global redis
    await redis.close()


def convert_ttl_to_seconds(ttl: str) -> int:
    ttl = ttl.lower()
    now = datetime.now()

    if ttl.endswith("m"):
        # 以月为单位
        months = int(ttl[:-1])
        future = now + timedelta(days=30 * months)
    elif ttl.endswith("w"):
        # 以星期为单位
        weeks = int(ttl[:-1])
        future = now + timedelta(weeks=weeks)
    elif ttl.endswith("d"):
        # 以天为单位
        days = int(ttl[:-1])
        future = now + timedelta(days=days)
    else:
        raise ValueError("Invalid TTL format. Please use 'm' for month, 'w' for week, 'd' for day.")

    ttl_seconds = int((future - now).total_seconds())
    return ttl_seconds


# 以月为单位：例如 "1m" 表示一个月的过期时间。
# 以星期为单位：例如 "2w" 表示两周的过期时间。
# 以天为单位：例如 "3d" 表示三天的过期时间。

REDIS_EXPIRATION_TIME = convert_ttl_to_seconds('1d')
