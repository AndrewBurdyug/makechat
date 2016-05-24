FROM python:3.5-slim
MAINTAINER Andrew Burdyug <buran83@gmail.com>
RUN pip --no-cache-dir install -U makechat
VOLUME /backups
EXPOSE 8000
CMD ["makechat", "backend", "run"]
