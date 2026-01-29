# Use an official Python runtime as a parent image
FROM python:3.10

RUN pip install --no-cache-dir rpyc
# Use for caching service
# RUN pip install --no-cache-dir rpyc redis

# Set the working directory
WORKDIR /app

COPY server.py .
COPY sample.txt .
COPY Fable.txt .

EXPOSE 4242

# Run the server (replace 'app.py' with your server script)
CMD ["python", "server.py"]