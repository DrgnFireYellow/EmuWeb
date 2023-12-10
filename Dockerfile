FROM nginx:latest
LABEL org.opencontainers.image.source="https://github.com/drgnfireyellow/emuweb"
COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY ./ /EmuWeb
WORKDIR /EmuWeb
EXPOSE 80
RUN apt-get update && apt-get install -y python3 && apt clean
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
