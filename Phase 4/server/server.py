import os
import redis
import rpyc
import logging
from rpyc import Service
from rpyc.utils.server import ThreadedServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

class WordCountService(Service):
    def exposed_wordcountingservice(self, ref, word):
        cache_key = f"{ref}:{word.lower()}"
        
        # Check cache
        cached = redis.get(cache_key)
        if cached is not None:
            # logger.info(f"Cache hit: {cache_key} = {cached}")
            return int(cached)
        
        # Otherwise, compute word count
        # logger.info(f"Cache miss for {cache_key}, computing word count")
        count = self.word_count(ref, word)
        
        # Store in cache
        redis.set(cache_key, count)
        # logger.info(f"Cache miss: storing {cache_key} = {count}")
        
        return count

    def word_count(self, ref, word):
        with open(ref, 'r') as f:
            text = f.read().lower()
        count = text.split().count(word.lower())
        redis.set(f"{ref}:{word.lower()}", count)
        return count

if __name__ == "__main__":
    server = ThreadedServer(WordCountService, hostname="0.0.0.0", port=4000)
    # logger.info(f"Server running on 0.0.0.0:4000")
    server.start()