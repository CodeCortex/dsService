import redis
import os
import json


class RedisService:

    def __init__(self):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", "6379"))

        print(f"Redis connecting to {host}:{port}")

        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

        try:
            self.client.ping()
            print(f"Redis connected successfully: {host}:{port}")
        except redis.ConnectionError as e:
            print(f"Redis connection failed: {host}:{port}")
            print(e)

    def get(self, key):
        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set(self, key, value, ttl=300):
        self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )

    def delete(self, key):
        self.client.delete(key)