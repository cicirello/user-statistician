# Copyright (c) 2021 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License

# The base image is pyaction:4, which is python:3-slim, plus the GitHub CLI (gh).
FROM ghcr.io/cicirello/pyaction:4

# Copy the GraphQl queries and python source into the container.
COPY src /

# Set the entrypoint.
ENTRYPOINT ["/UserStatistician.py"]
