FROM nginx:1.25.3
LABEL org.opencontainers.image.source="https://github.com/drgnfireyellow/emuweb"
COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY ./ /EmuWeb
WORKDIR /EmuWeb
EXPOSE 80
RUN apt-get update && apt-get install -y --no-install-recommends python3 && apt clean && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
