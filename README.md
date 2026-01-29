# Distributed Word Count Service

## Overview

This project implements a distributed word count service designed to explore key concepts in distributed systems, including scalability, caching, load balancing, and fault tolerance.

Clients query how many times a given word appears in a text document. Requests are handled by a set of application servers, cached using Redis, and distributed across servers via a load balancer.

## Architecture

The system follows a client–server architecture with a shared in-memory cache and a load balancer.

Components:
- **Client**: Sends word count requests.
- **Load Balancer**: Distributes requests using Round Robin or Two-Choice algorithms.
- **Servers**: Process word count requests and interact with the cache.
- **Redis**: Caches previously computed results to reduce latency.

The architecture evolves across multiple phases to progressively introduce scalability and fault tolerance.

## Technologies

- Python
- RPyc (RPC communication)
- Redis (in-memory caching)
- Docker & Docker Compose

## Load Balancing

Two load balancing strategies are implemented:

- **Round Robin**: Requests are distributed sequentially across servers.
- **Two-Choice**: Two servers are randomly sampled, and the least loaded one is selected.

Both strategies are evaluated in terms of runtime and scalability.

## Fault Tolerance

The load balancer periodically performs health checks on servers.
Unresponsive servers are removed from the pool of healthy servers, ensuring continued service availability in case of failure.

## Performance & Evaluation

The system is evaluated under multiple configurations:
- Single server vs cached server
- Multiple servers with load balancing
- Server failure scenarios

Results show that caching and load balancing introduce overhead for small workloads, but become beneficial as workload complexity and scale increase.

## Credits

Developed by:
- Angelo Filiol de Raimond
- Jules Anseaume

As part of the MSc Computer Science and Engineering program at TU Eindhoven.


