FROM nginx:alpine

RUN mkdir -pv /etc/nginx/sites-available/ && \
    mkdir -pv /etc/nginx/sites-enabled/

RUN mkdir -pv /var/run/ && \
    chown -R nginx:nginx /var/run/

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY nivalta.conf /etc/nginx/sites-available/nivalta.conf

RUN ln -s /etc/nginx/sites-available/nivalta.conf /etc/nginx/sites-enabled

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]