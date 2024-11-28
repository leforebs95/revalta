#!/bin/sh

# Function to check DNS resolution
check_dns() {
    local host=$1
    echo "Checking DNS resolution for $host..."

    # Try multiple DNS lookup tools in case one isn't available
    if command -v dig >/dev/null; then
        dig +short $host || return 1
    elif command -v nslookup >/dev/null; then
        nslookup $host || return 1
    elif command -v drill >/dev/null; then
        drill $host || return 1
    else
        echo "No DNS lookup tools available"
        return 0 # Continue anyway as this is just a check
    fi
}

# Initial delay to allow services to start
echo "Waiting for services to be ready..."
sleep 5

# Check service resolution
check_dns ${FLASK_SERVICE_HOST} || echo "Warning: Could not resolve Flask service"
check_dns ${SVELTE_SERVICE_HOST} || echo "Warning: Could not resolve Svelte service"

# Generate nginx configuration
echo "Generating Nginx configuration..."
envsubst '$FLASK_SERVICE_HOST $SVELTE_SERVICE_HOST' </etc/nginx/nginx.template.conf >/etc/nginx/nginx.conf

# Verify configuration
echo "Verifying Nginx configuration..."
nginx -t || exit 1

# Start nginx
echo "Starting Nginx..."
nginx -g 'daemon off;'
