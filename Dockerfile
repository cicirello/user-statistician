# Copyright (c) 2021-2022 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License

# The base image is pyaction, which is python slim, plus the GitHub CLI (gh).
FROM ghcr.io/cicirello/pyaction:4.14.0

# Copy the GraphQl queries and python source into the container.
COPY src /

# Set the entrypoint.
ENTRYPOINT ["/UserStatistician.py"]
