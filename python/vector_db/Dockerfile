ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files and enables unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app
ENV ENVIRONMENT=development

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-privileged user with a proper home directory
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/bin/bash" \
    --uid "${UID}" \
    appuser

# Create necessary directories with correct permissions
RUN mkdir -p /var/log/gunicorn/ && \
    chown -R appuser:appuser /var/log/gunicorn/ && \
    chmod 755 /var/log/gunicorn/ && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /home/appuser && \
    chmod 755 /home/appuser

# Copy requirements first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and config files
COPY --chown=appuser:appuser . .

# Copy and set up entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

# Switch to non-privileged user
USER appuser

# Expose the application port
EXPOSE 5003

# Use entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app()"]