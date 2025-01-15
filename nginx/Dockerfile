FROM nginx:alpine


# Install necessary tools
RUN apk add --no-cache drill bind-tools

# Create required temp directories for file uploads
RUN mkdir -p /tmp/nginx/client_temp && \
    mkdir -p /tmp/nginx/proxy_temp && \
    mkdir -p /tmp/nginx/fastcgi_temp && \
    chown -R nginx:nginx /tmp/nginx && \
    chmod -R 755 /tmp/nginx

COPY ./nginx.template.conf /etc/nginx/nginx.template.conf

# Add a script to run before starting nginx
COPY ./start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh

CMD ["/start-nginx.sh"]