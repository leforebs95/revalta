#!/bin/bash
set -e

# Function to wait for a service
wait_for_service() {
    local host="$1"
    local port="$2"
    local service="$3"
    local retries=5
    local wait=5
    
    echo "Testing connection to $service at $host:$port..."
    
    for i in $(seq 1 $retries); do
        nc -z "$host" "$port" && echo "$service is up!" && return 0
        echo "Waiting for $service to be ready... $i/$retries"
        sleep "$wait"
    done
    
    echo "Error: $service is not available!"
    return 1
}

# Wait for required services in non-development environments
if [ "$ENVIRONMENT" != "development" ]; then
    # Wait for database
    wait_for_service "uploads-db" 5432 "PostgreSQL"
fi

# Create log directories if they don't exist (for production)
if [ "$ENVIRONMENT" = "production" ]; then
    mkdir -p /var/log/gunicorn
fi

# Run database migrations if needed
if [ "$ENVIRONMENT" != "development" ]; then
    flask db upgrade
fi

# Execute the main container command
exec "$@" 