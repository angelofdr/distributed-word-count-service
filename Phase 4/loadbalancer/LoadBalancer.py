import asyncio
import os
from collections import defaultdict
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of servers
SERVERS = {
    "server1": 4000,
    "server2": 4001,
    "server3": 4002
}

# Load balancing algo
Algo = "Two-Sampling"  # Options: "Round-Robin", "Two-Sampling"
index = 0
SERVER_NAMES = list(SERVERS.keys())
logger.info(f"Servers: {SERVER_NAMES}")
server_connections = {server: 0 for server in SERVER_NAMES}

# Health status tracking
healthy_servers = {server: True for server in SERVER_NAMES}  # Initially all healthy

# Health check interval (in seconds)
HEALTH_CHECK_INTERVAL = 5

async def health_check(server_name, server_port):
    """Try to connect to the server to check if it's healthy."""
    try:
        reader, writer = await asyncio.open_connection(server_name, server_port)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False

async def health_check_loop():
    """Background loop to periodically check server health."""
    while True:
        for server in SERVER_NAMES:
            port = SERVERS[server]
            is_healthy = await health_check(server, port)
            if healthy_servers[server] != is_healthy:
                healthy_servers[server] = is_healthy
                status = "healthy" if is_healthy else "unhealthy"
                logger.info(f"Health check: {server} is now {status}")
        await asyncio.sleep(HEALTH_CHECK_INTERVAL)

def get_healthy_server_names():
    """Get list of currently healthy servers."""
    return [s for s in SERVER_NAMES if healthy_servers[s]]

async def transfer_data(source, destination):
    try:
        while data := await source.read(4096):
            destination.write(data)
            await destination.drain()
    except Exception as e:
        logger.error(f"Error during data transfer: {e}")
    finally:
        destination.close()

def pick_server():
    global Algo, index
    healthy = get_healthy_server_names()
    if not healthy:
        raise ValueError("No healthy servers available")

    if Algo == "Round-Robin":
        server = healthy[index % len(healthy)]
        index = (index + 1) % len(SERVER_NAMES)  # Cycle through all, but pick from healthy
        return server
    elif Algo == "Two-Sampling":
        if len(healthy) < 2:
            return healthy[0] if healthy else None
        s1, s2 = random.sample(healthy, 2)
        if server_connections[s1] <= server_connections[s2]:
            return s1
        else:
            return s2
    else:
        return healthy[0] if healthy else None

async def handle_request(client_reader, client_writer):
    try:
        server = pick_server()
    except ValueError as e:
        logger.error(f"Cannot handle request: {e}")
        client_writer.close()
        await client_writer.wait_closed()
        return

    # Use line underneath for logging which server is picked for presentation purposes
    logger.info(f"Forwarding request to {server} (Algo: {Algo})")
    server_connections[server] += 1
    server_name = server
    server_port = SERVERS[server]

    try:
        server_reader, server_writer = await asyncio.open_connection(server_name, server_port)
    except Exception as e:
        logger.error(f"Error connecting to {server}: {e}. Marking as unhealthy.")
        healthy_servers[server] = False
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

    # Start health check loop in background
    asyncio.create_task(health_check_loop())

    server = await asyncio.start_server(
        handle_request, host, port
    )

    logger.info("LoadBalancer ready with fault tolerance!")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
