# syntax=docker/dockerfile:1
FROM python:3.10-alpine AS base

ARG APP_USER=anvil
ARG APP_UID=1000
RUN addgroup -S ${APP_USER} \
 && adduser -S -G ${APP_USER} -u ${APP_UID} ${APP_USER} \
 && mkdir -p /home/${APP_USER} \
 && chown -R ${APP_USER}:${APP_USER} /home/${APP_USER}

ENV HOME=/home/${APP_USER}
ENV PATH=/usr/local/bin:$PATH

# Create a working directory
WORKDIR /app

# Expose default anvil port
EXPOSE 3030

# Install required dependencies: openjdk8, git, ssh (for cloning), bash, etc.
RUN apk add --no-cache \
      openjdk11 \
      git \
      openssh-client \
      bash \
      curl \
      gcc musl-dev linux-headers \
      && python3 -m pip install --no-cache-dir --upgrade pip

USER anvil
RUN pip install --no-cache-dir anvil-app-server \
    && pip install --no-cache-dir phoenix_a3000_verify@git+https://github.com/Quik2007/phoenix_a3000_verify.git
USER root

# Clone public repo
RUN git clone https://github.com/anvil-works/routing \
    && mv routing 3PIDO5P3H4VPEMPL

# Clone private repo with SSH mount
RUN --mount=type=ssh \
    mkdir -p -m 0700 /root/.ssh \
    && ssh-keyscan -p 2222 anvil.works >> /root/.ssh/known_hosts \
    && git clone ssh://quintenwolff%40outlook.de@anvil.works:2222/LT5M56WDZC6O5IVA.git

# Create app dir and set permissions
RUN chown -R ${APP_USER}:${APP_USER} /app

# Switch to app user
USER ${APP_USER}
ENV PATH=/home/${APP_USER}/.local/bin:$PATH

# Default command: run anvil-app-server with your app
CMD anvil-app-server --database jdbc:postgresql://postgres/anvil?user=anvil --app LT5M56WDZC6O5IVA --port 3030
