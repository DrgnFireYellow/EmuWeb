FROM caddy:alpine
LABEL org.opencontainers.image.source="https://github.com/drgnfireyellow/emuweb"
LABEL maintainer="DrgnFireYellow"
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY ./ /EmuWeb
COPY Caddyfile /etc/caddy/Caddyfile
WORKDIR /EmuWeb
EXPOSE 80 443
RUN apk update && apk add python3 py3-pip && apk cache clean && python3 -m pip install -r /EmuWeb/requirements.txt --break-system-packages
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
