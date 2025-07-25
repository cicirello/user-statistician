# Copyright (c) 2021-2025 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License

# The base image is pyaction, which is python slim, plus the GitHub CLI (gh).
FROM ghcr.io/cicirello/pyaction:3.13.5-gh-2.76.1

# Copy the GraphQl queries and python source into the container.
COPY src /

# Set the entrypoint.
ENTRYPOINT ["/UserStatistician.py"]
