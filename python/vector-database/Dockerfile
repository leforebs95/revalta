ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add curl for healthcheck
RUN apt-get update && apt-get install -y curl

WORKDIR /usr/src/vector-service

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create necessary directories with correct permissions
RUN mkdir -p /var/log/gunicorn/ && \
    chown -R appuser:appuser /var/log/gunicorn/ && \
    chmod 755 /var/log/gunicorn/

# Copy the source code
COPY --chown=appuser:appuser . .

ENV PYTHONPATH=/usr/src/vector-service

# Download dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r /usr/src/vector-service/requirements.txt

# Switch to non-privileged user
USER appuser

EXPOSE 5003

CMD [ "gunicorn", "-c", "gunicorn_dev.py" ]