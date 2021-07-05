# Copyright (c) 2021 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License

# Base image, pyaction:4, which is python:3-slim, plus the GitHub CLI (gh).
FROM ghcr.io/cicirello/pyaction:4

# Copy the GraphQl queries and python source into the container.
COPY queries /queries
COPY UserStatistician.py /UserStatistician.py

# Set the entrypoint.
ENTRYPOINT ["/UserStatistician.py"]
