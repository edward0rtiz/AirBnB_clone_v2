#!/usr/bin/env bash
apt-get update
apt-get install -y nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared
echo "Test deployment" | sudo tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
config='\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;}'
sed -i "12i $config" /etc/nginx/sites-available/default
service nginx restart
