import redis
import redis.asyncio as aioredis
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Redis Client connection details
REDIS_URL = settings.REDIS_URL

class RedisClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._init_redis()
        return cls._instance
        
    def _init_redis(self):
        try:
            self.client = redis.from_url(REDIS_URL, decode_responses=True)
            self.client.ping()
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            self.client = None

    def get_client(self):
        if self.client is None:
            logger.warning("Redis client is not initialized, attempting to reconnect...")
            self._init_redis()
        return self.client

redis_client = RedisClient().get_client()

# Async Redis Client for async operations
try:
    async_redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
except Exception as e:
    logger.error(f"Async Redis connection error: {e}")
    async_redis_client = None

def get_redis_client():
    """Return an asynchronous Redis client."""
    return async_redis_client
