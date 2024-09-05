#!/bin/sh

# Set Flask and Svelete host - Allows for localhost in ECS and Container names locally
echo "Setting $FLASK_HOST and $SVELTE_HOST in Nginx configuration..."
envsubst '$FLASK_HOST $SVELTE_HOST' </etc/nginx/nginx.template.conf >/etc/nginx/nginx.conf

# Start nginx
echo "Starting Nginx..."
nginx -g 'daemon off;'
