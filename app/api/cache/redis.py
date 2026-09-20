import json
from redis import Redis


class RedisCacheBackend:

    def __init__(self, redis_url:str, cache_ttl_sec: int | None):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_sec

    def set(self, key, value:dict) -> None:
        self.redis.set(
            key,
            json.dumps(value),
            ex=self.cache_ttl_seconds,
            )

    def get(self, key: str) -> dict:
        value = self.redis.get(key)
        return json.loads(value) if value is not None else None

    def delete(self, key) -> None:
        self.redis.delete(key)