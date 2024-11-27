#!/bin/sh

# Set Flask and Svelete host - Allows for localhost in ECS and Container names locally
echo "Setting $FLASK_SERVICE_HOST and $SVELTE_SERVICE_HOST in Nginx configuration..."
envsubst '$FLASK_SERVICE_HOST $SVELTE_SERVICE_HOST' </etc/nginx/nginx.template.conf >/etc/nginx/nginx.conf

# Start nginx
echo "Starting Nginx..."
nginx -g 'daemon off;'
