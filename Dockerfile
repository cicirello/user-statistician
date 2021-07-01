FROM cicirello/pyaction-lite:latest
# FROM cicirello/pyaction:latest
# FROM ghcr.io/cicirello/pyaction-lite:latest
# FROM ghcr.io/cicirello/pyaction:latest

COPY UserStatistician.py /UserStatistician.py
ENTRYPOINT ["/UserStatistician.py"]
