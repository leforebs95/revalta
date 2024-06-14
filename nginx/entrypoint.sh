#!/bin/sh

# Read the SSL secrets from the Docker secrets files
export SSL_CERTIFICATE=$(cat /run/secrets/ssl_certificate)
export SSL_CERTIFICATE_KEY=$(cat /run/secrets/ssl_certificate_key)

# Substitute environment variables in the Nginx configuration template
envsubst '$SSL_CERTIFICATE $SSL_CERTIFICATE_KEY' </etc/nginx/nginx.conf.template >/etc/nginx/nginx.conf

# Start Nginx
nginx -g 'daemon off;'
