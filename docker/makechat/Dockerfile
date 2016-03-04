FROM python:3.5
MAINTAINER Andrew Burdyug <buran83@gmail.com>
RUN easy_install makechat
VOLUME /backups /etc/makechat.conf
EXPOSE 8000
CMD ["makechat", "run_server"]
