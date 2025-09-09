# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine AS base

# Install required dependencies: openjdk8, git, ssh (for cloning), bash, etc.
RUN apk add --no-cache \
      openjdk8 \
      git \
      openssh-client \
      bash \
      curl \
      gcc musl-dev linux-headers \
      openssh \
      && python3 -m pip install --no-cache-dir --upgrade pip \
      && pip install --no-cache-dir anvil-app-server

# Create a working directory
WORKDIR /app

# Clone repos
RUN git clone https://github.com/anvil-works/routing \
    && mv routing 3PIDO5P3H4VPEMPL

RUN --mount=type=secret,id=ssh_key \
    mkdir -p /root/.ssh \
    && cp /run/secrets/ssh_key /root/.ssh/id_key \
    && chmod 600 /root/.ssh/id_key \
    && ssh-keyscan -p 2222 anvil.works >> /root/.ssh/known_hosts \
    && GIT_SSH_COMMAND="ssh -i /root/.ssh/id_key -o IdentitiesOnly=yes" \
       git clone ssh://quintenwolff%40outlook.de@anvil.works:2222/LT5M56WDZC6O5IVA.git \
    && rm -f /root/.ssh/id_key

# Default command: run anvil-app-server with your app
CMD ["anvil-app-server", "--app", "LT5M56WDZC6O5IVA"]
