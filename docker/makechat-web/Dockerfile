FROM nginx:latest
MAINTAINER Andrew Burdyug <buran83@gmail.com>

RUN mkdir -pv /etc/nginx/makechat
RUN mkdir -pv /usr/share/nginx/html/makechat/default

ADD makechat_vhost.conf /etc/nginx/makechat/
ADD makechat_maintenance_vhost.conf /etc/nginx/makechat/
ADD maintenance /usr/local/sbin/

COPY html/ /usr/share/nginx/html/makechat/default/
COPY js/ /usr/share/nginx/html/makechat/default/

RUN ln -s  /etc/nginx/makechat/makechat_vhost.conf /etc/nginx/conf.d/makechat_vhost.conf

VOLUME /usr/share/nginx/html/makechat/custom
