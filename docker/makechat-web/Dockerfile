FROM nginx:latest
MAINTAINER Andrew Burdyug <buran83@gmail.com>

RUN mkdir -pv /etc/nginx/makechat

ADD makechat_vhost.conf /etc/nginx/makechat/
ADD makechat_maintenance_vhost.conf /etc/nginx/makechat/
ADD maintenance.html /usr/share/nginx/html/
ADD maintenance /usr/local/sbin/

RUN ln -s  /etc/nginx/makechat/makechat_vhost.conf /etc/nginx/conf.d/makechat_vhost.conf
