FROM python:3.5
MAINTAINER Andrew Burdyug <buran83@gmail.com>
RUN pip --no-cache-dir install -U makechat
VOLUME /backups
EXPOSE 8000
CMD ["uwsgi", "--ini", "/root/makechat.conf"]
