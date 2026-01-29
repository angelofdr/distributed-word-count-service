FROM python:3.10

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip install --no-cache-dir rpyc
RUN pip install --no-cache-dir rpyc redis

WORKDIR /app

COPY LoadBalancer.py ./

EXPOSE 12345

CMD ["python3", "-u", "LoadBalancer.py"]