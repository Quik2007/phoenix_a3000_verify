# syntax=docker/dockerfile:1
FROM python:3.10-alpine AS base

# Install required dependencies: openjdk8, git, ssh (for cloning), bash, etc.
RUN apk add --no-cache \
      openjdk8 \
      git \
      openssh-client \
      bash \
      curl \
      gcc musl-dev linux-headers \
      && python3 -m pip install --no-cache-dir --upgrade pip \
      && pip install --no-cache-dir anvil-app-server

# Create a working directory
WORKDIR /app

# Clone public repo
RUN git clone https://github.com/anvil-works/routing \
    && mv routing 3PIDO5P3H4VPEMPL

# Clone private repo with SSH mount
RUN --mount=type=ssh \
    mkdir -p -m 0700 /root/.ssh \
    && ssh-keyscan -p 2222 anvil.works >> /root/.ssh/known_hosts \
    && git clone ssh://quintenwolff%40outlook.de@anvil.works:2222/LT5M56WDZC6O5IVA.git

# Default command: run anvil-app-server with your app
CMD ["anvil-app-server", "--app", "LT5M56WDZC6O5IVA"]
