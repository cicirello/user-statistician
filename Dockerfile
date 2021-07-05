FROM ghcr.io/cicirello/pyaction:4

COPY queries /queries
COPY UserStatistician.py /UserStatistician.py
ENTRYPOINT ["/UserStatistician.py"]
