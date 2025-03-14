FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create log directory for production
RUN mkdir -p /var/log/gunicorn && \
    chown -R nobody:nogroup /var/log/gunicorn

# Copy application code and gunicorn config
COPY . .

# Set environment variables
ENV FLASK_APP=app
ENV ENVIRONMENT=development
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER nobody

# Expose port
EXPOSE 5000

# Use entrypoint script for initialization
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command (can be overridden)
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app()"] 