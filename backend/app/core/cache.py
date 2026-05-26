import redis

from decouple import config


# =====================================================
# REDIS CONFIG
# =====================================================

REDIS_HOST = config(
    "REDIS_HOST",
    default="localhost"
)

REDIS_PORT = config(
    "REDIS_PORT",
    default=6379,
    cast=int
)

REDIS_DB = config(
    "REDIS_DB",
    default=0,
    cast=int
)


# =====================================================
# CREATE REDIS CLIENT SAFELY
# =====================================================

cache = None

try:

    cache = redis.Redis(

        host=REDIS_HOST,

        port=REDIS_PORT,

        db=REDIS_DB,

        decode_responses=True
    )

    cache.ping()

    print("✅ Redis connected")

except Exception as e:

    print(f"⚠️ Redis unavailable: {e}")

    cache = None


# =====================================================
# CACHE HELPERS
# =====================================================

def set_cache(key: str, value: str, expire: int = 300):

    if cache:

        cache.setex(key, expire, value)


def get_cache(key: str):

    if cache:

        return cache.get(key)

    return None


def delete_cache(key: str):

    if cache:

        cache.delete(key)