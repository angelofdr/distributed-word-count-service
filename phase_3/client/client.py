import os
import threading
import rpyc
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

word_to_count = [
    ("sample.txt", "the"),
    ("sample.txt", "and"),
    ("sample.txt", "wisdom"),
    ("sample.txt", "the"),
    ("sample.txt", "truth"),
    ("sample.txt", "virtue"),
    ("sample.txt", "lesson"),
    ("sample.txt", "moral"),
    ("sample.txt", "kindness"),
    ("sample.txt", "honor"),
    ("sample.txt", "friendship"),
    ("sample.txt", "courage"),
    ("sample.txt", "life"),
    ("sample.txt", "knowledge"),
    ("Fable.txt", "ant"),
    ("Fable.txt", "lion"),
    ("Fable.txt", "the"),
    ("Fable.txt", "and"),
    ("Fable.txt", "wisdom"),
    ("Fable.txt", "the"),
    ("Fable.txt", "strength"),
    ("Fable.txt", "clever"),
    ("Fable.txt", "forest"),
    ("Fable.txt", "hunter"),
    ("Fable.txt", "escape"),
    ("Fable.txt", "danger"),
    ("Fable.txt", "victory"),
    ("Fable.txt", "trust"),
]

# Get host/port from environment variables (set in docker-compose.yml)
loadbalancer_host = os.getenv("LOADBALANCER_HOST", "loadbalancer")
loadbalancer_port = int(os.getenv("LOADBALANCER_PORT", "12345"))

# Connect to the RPyC server
# logger.info(f"Connected to RPyC server at {server_host}:{server_port}")

def wordcountingclient(ref: str, word: str, c):
    # Call remote method via .root
    result = c.root.wordcountingservice(ref, word)
    logger.info(result)

# Use to print all words and durations for visualization
def print_results(durations):
    print("\nWord Count Results and Durations:")
    for word, duration in durations:
        print(word, duration)


if __name__ == "__main__":
    durations = []
    c = rpyc.connect(loadbalancer_host, loadbalancer_port)
    for (file_ref, word) in word_to_count:
        start_time = time.time() #Get delay between request send and receive
        wordcountingclient(file_ref, word, c)
        end_time = time.time()
        logger.info(f"Request for '{word}' in file '{file_ref}' completed in {end_time - start_time:.4f} seconds")
        durations.append([word, end_time - start_time])
    # Use this line to print all results and durations
    #print_results(durations)
    # logger.info("All requests completed.")