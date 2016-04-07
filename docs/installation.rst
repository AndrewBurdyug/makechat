===============
Getting started
===============

###################
System requirements
###################
* Docker
* MongoDb
* Python 3.x

**Makechat** will store all data(accounts/rooms/messages etc) into *MongoDb*,
for easy setup we use docker containers, you do not warry about complecated
setup procedures.

############
Installation
############
Make these steps:

#. `Install docker <https://docs.docker.com/engine/installation/>`_
#. Run docker containers::

    $ sudo mkdir -pv /makechat-backups /var/lib/makechat-mongo /var/www/makechat
    $ sudo chmod 700 /makechat-backups /var/lib/makechat-mongo
    $ echo "172.30.1.1 makechat-mongo" | sudo tee --append /etc/hosts
    $ echo "172.30.1.2 makechat" | sudo tee --append /etc/hosts
    $ echo "172.30.1.3 makechat-web" | sudo tee --append /etc/hosts
    $ docker network create -d bridge --subnet 172.30.0.0/16 makechat_nw
    $ docker run --net=makechat_nw --ip=172.30.1.1 -v /var/lib/makechat-mongo:/data/db \
        --name makechat-mongo -d mongo:latest
    $ docker run --net=makechat_nw --ip=172.30.1.2 -v /makechat-backups:/backups \
        --name makechat -d buran/makechat:latest
    $ docker run --net=makechat_nw --ip=172.30.1.3 --name makechat-web \
        -v /var/www/makechat:/usr/share/nginx/html/makechat/custom \
        -d buran/makechat-web:latest

#. Edit ``~/makechat.conf``

    .. note::
        Currently ``makechat.conf`` placed inside home directory of user
        who installed the **makechat** python package.

#. Restart backend::

    $ docker restart makechat

#. Go to ``http://youdomain.com/makechat/admin`` and create user accounts/rooms
