# syntax=docker/dockerfile:1.4
###############################################################################
# Builder stage - install build deps, pip install anvil-app-server, clone repos
###############################################################################
FROM python:3.10-alpine AS builder

# Install build-time dependencies (git, ssh for clone, build deps for wheels)
RUN apk add --no-cache \
      openjdk8 \
      git \
      openssh-client \
      bash \
      curl \
      gcc \
      musl-dev \
      linux-headers \
      && python3 -m pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Clone public repo (routing) and rename
RUN git clone https://github.com/anvil-works/routing \
    && mv routing 3PIDO5P3H4VPEMPL

# Install anvil-app-server into the image (system location /usr/local)
# installing here keeps runtime stage lighter (we'll copy /usr/local into runtime)
RUN pip install --no-cache-dir anvil-app-server

# Clone the private repo using SSH agent forwarding (BuildKit ssh mount)
# NOTE: this command expects the build command to forward SSH agent (ssh: default)
# We also add the host key to known_hosts to avoid host prompt.
RUN --mount=type=ssh \
    set -eux; \
    mkdir -p /root/.ssh && chmod 700 /root/.ssh; \
    ssh-keyscan -p 2222 anvil.works >> /root/.ssh/known_hosts; \
    GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=yes" \
      git clone ssh://quintenwolff%40outlook.de@anvil.works:2222/LT5M56WDZC6O5IVA.git

###############################################################################
# Runtime stage - minimal runtime with non-root user
###############################################################################
FROM python:3.10-alpine AS runtime

# Runtime-only packages: JRE + small utilities (no git, no build tools)
RUN apk add --no-cache \
      openjdk8 \
      bash \
      curl \
    && rm -rf /var/cache/apk/*

# Create non-root user (UID 1000) and home
ARG APP_USER=appuser
ARG APP_UID=1000
RUN addgroup -S ${APP_USER} \
 && adduser -S -G ${APP_USER} -u ${APP_UID} ${APP_USER} \
 && mkdir -p /home/${APP_USER} \
 && chown -R ${APP_USER}:${APP_USER} /home/${APP_USER}

ENV HOME=/home/${APP_USER}
ENV PATH=/usr/local/bin:$PATH

# Create app dir and set permissions
RUN mkdir -p /app \
 && chown -R ${APP_USER}:${APP_USER} /app

WORKDIR /app

# Copy python packages and installed binaries from builder
# We copy /usr/local which contains pip-installed packages and scripts (anvil-app-server)
COPY --from=builder /usr/local /usr/local

# Copy the cloned app(s) from builder stage
COPY --from=builder /app /app

# Ensure correct ownership in final image
RUN chown -R ${APP_USER}:${APP_USER} /app /usr/local

# Expose default anvil port (adjust if you use a different port)
EXPOSE 3030

# Switch to non-root user
USER ${APP_USER}

# Default command — run anvil-app-server for the app folder cloned earlier
# Keep this format so Docker/Podman can override the command or pass args
CMD ["anvil-app-server", "--app", "LT5M56WDZC6O5IVA"]
