FROM python:3-slim

RUN apt-get update && apt-get install -y \
    gh \
    && rm -rf /var/lib/apt/lists/*

COPY UserStatistician.py /UserStatistician.py
ENTRYPOINT ["/UserStatistician.py"]
