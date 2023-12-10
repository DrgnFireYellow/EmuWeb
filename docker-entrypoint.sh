/usr/bin/python3 /EmuWeb/main.py
chmod 777 /EmuWeb/games
chmod 777 /EmuWeb/artwork
nginx -c /etc/nginx/nginx.conf -g "daemon off;"