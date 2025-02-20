ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add curl for healthcheck
RUN apt-get update && apt-get install -y curl

WORKDIR /usr/src/uploads

# Create a non-privileged user that the app will run under.
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
RUN mkdir -p /var/log/gunicorn/ /usr/src/uploads/uploads && \
    chown -R appuser:appuser /var/log/gunicorn/ /usr/src/uploads/uploads && \
    chmod 755 /var/log/gunicorn/ /usr/src/uploads/uploads

# Copy the source code into the container.
COPY --chown=appuser:appuser . .

ENV PYTHONPATH=/usr/src/uploads

# Download dependencies as a separate step to take advantage of Docker's caching.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r /usr/src/uploads/requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 5001

CMD [ "gunicorn", "-c", "gunicorn_dev.py" ]