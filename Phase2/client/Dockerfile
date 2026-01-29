# Use Python base image
FROM python:3.10

RUN pip install --no-cache-dir rpyc
# Use for caching service
# RUN pip install --no-cache-dir rpyc redis 

# Set working directory
WORKDIR /app

# Copy client code
COPY client.py .


# Run the client
CMD ["python", "client.py"]