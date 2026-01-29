import os
import rpyc
# import redis
import logging
import re
from rpyc import Service
from rpyc.utils.server import ThreadedServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use for caching service
# redis_host = os.getenv("REDIS_HOST", "redis")
# redis_port = int(os.getenv("REDIS_PORT", "6379"))
# redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

class WordCountService(Service):
    def exposed_wordcountingservice(self, ref, word):
        # Uncomment all lines that contain the word "cache" and some type of action to also use the redis cache (also uncomment in docker compose file)
        # cache_key = f"{ref}:{word.lower()}"
        
        # Check cache
        # cached = redis.get(cache_key)
        # if cached is not None:
        #     logger.info(f"Cache hit: {cache_key} = {cached}")
        #     return int(cached)
        
        # Otherwise, compute word count
        # logger.info(f"Cache miss for {cache_key}, computing word count")
        count = self.word_count(ref, word)
        
        # Store in cache
        # redis.set(f"{ref}:{word.lower()}", count)
        # logger.info(f"Cache miss: storing {cache_key} = {count}")
        
        return count

    def word_count(self, ref, word):
        with open(ref, 'r') as f:
            text = f.read().lower()
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        
        matches = re.findall(pattern, text)
        count = len(matches)
        return count

if __name__ == "__main__":
    server = ThreadedServer(WordCountService, hostname="0.0.0.0", port=4242)
    # logger.info(f"Server running on 0.0.0.0:4242")
    server.start()