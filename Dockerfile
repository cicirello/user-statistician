FROM python:3-slim

RUN true \
    && apt-get update && apt-get install -y \
       curl \
       gpg \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update && apt-get install -y \
       gh \
    && rm -rf /var/lib/apt/lists/* \
    && true

COPY queries /queries
COPY UserStatistician.py /UserStatistician.py
ENTRYPOINT ["/UserStatistician.py"]
