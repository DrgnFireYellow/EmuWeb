FROM nginx:1.25.3
LABEL org.opencontainers.image.source="https://github.com/drgnfireyellow/emuweb"
LABEL maintainer="DrgnFireYellow"
COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY ./ /EmuWeb
WORKDIR /EmuWeb
EXPOSE 80
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && apt clean && rm -rf /var/lib/apt/lists/* && python3 -m pip install -r /EmuWeb/requirements.txt
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
