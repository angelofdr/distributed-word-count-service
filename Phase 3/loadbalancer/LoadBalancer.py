import asyncio
import os
from collections import defaultdict
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of servers from env vars
SERVERS = {
    "server1":4000,
    "server2":4000,
    "server3":4000
}

# Load balancing algo
Algo = "Two-Sampling"  # Options: "Round-Robin", "Two-Sampling"
index = 0
SERVER_NAMES = list(SERVERS.keys())
logger.info(f"Servers: {SERVER_NAMES}")
server_connections = {server: 0 for server in SERVER_NAMES}

async def transfer_data(source, destination):
    try:
        while data := await source.read(4096):
        # Get response from server and send back to client
            destination.write(data)
            await destination.drain()
    except Exception as e:
        print(f"Error during data transfer from {source}: {e}")
    finally:
        destination.close()

def pick_server():
    global Algo, index
    if Algo == "Round-Robin":
        server = SERVER_NAMES[index]
        index = (index + 1) % len(SERVER_NAMES)
        return server
    elif Algo == "Two-Sampling": #Use two sampling
        # pick two distinct server indices
        s1, s2 = random.sample(range(len(SERVER_NAMES)), 2)
        if server_connections[SERVER_NAMES[s1]] <= server_connections[SERVER_NAMES[s2]]:
            return SERVER_NAMES[s1]
        else:
            return SERVER_NAMES[s2]
    else:
        return "server1"

async def handle_request(client_reader, client_writer):
    server = pick_server()
    # Use line underneath for logging which server is picked for presentation purposes
    # logger.info(f"Forwarding request to {server}")
    server_connections[server] += 1
    server_name = server
    server_port = SERVERS[server]

    try:
        server_reader, server_writer = await asyncio.open_connection(server_name, server_port)
    except Exception as e:
        logger.error(f"Error connecting to {server}: {e}")
        client_writer.close()
        await client_writer.wait_closed()
        return
    
    try:
        await asyncio.gather(
            transfer_data(client_reader, server_writer),
            transfer_data(server_reader, client_writer)
        )
    finally:
        server_connections[server] -= 1
        # logger.info(f"Connection to {server_name}:{server_port} closed")
    
    

async def main():
    host = os.getenv("LOADBALANCER_HOST", "0.0.0.0")
    port = int(os.getenv("LOADBALANCER_PORT", "12345"))

    server = await asyncio.start_server(
        handle_request, host, port
    )

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    print("LoadBalancer ready!")
    asyncio.run(main())
