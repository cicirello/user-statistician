FROM ghcr.io/cicirello/pyaction:

COPY queries /queries
COPY UserStatistician.py /UserStatistician.py
ENTRYPOINT ["/UserStatistician.py"]
