FROM nginx:alpine

# Install necessary tools
RUN apk add --no-cache drill bind-tools

COPY ./nginx.template.conf /etc/nginx/nginx.template.conf

# Add a script to run before starting nginx
COPY ./start-nginx.sh /start-nginx.sh
RUN chmod +x /start-nginx.sh

CMD ["/start-nginx.sh"]