import redis
from config.settings import get_settings

# 설정 가져오기
settings = get_settings()

# Redis 클라이언트 생성
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)


def get_redis() -> redis.Redis:
    """Redis 클라이언트 반환"""
    return redis_client