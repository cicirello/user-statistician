FROM cicirello/pyaction-lite:latest
# FROM cicirello/pyaction:latest
# FROM ghcr.io/cicirello/pyaction-lite:latest
# FROM ghcr.io/cicirello/pyaction:latest

COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
