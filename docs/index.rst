========
Overview
========
There are many chat programs, but almost all of them have the same
disadvantages:

* not open sourse, possible have many hidden bugs/leaks
* you can not run own chat server and use it for own aims, you should use
  central server which you can not control, it is bad:

    * it may not working properly or restrict connections by country due to
      sanctions, for example HipChat is blocking Crimean users
    * your private messages/accounts could fall into the wrong hands,
      because you can't control how the central server is safe

In some cases, if your work is depent on chat systems and you need to have it
working without unexpected outage, these desadvantages unacceptable for you.
**Makechat** provide you simple chat system, which you might fully control.
You might create public/private chat rooms, write your own notifier/bot etc,
easy move/run your chat server to anywhere, where Docker works.

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

    $ sudo mkdir /var/lib/mongo && sudo chmod 700 /var/lib/mongo
    $ sudo mkdir /backups && sudo chmod 700 /backups
    $ docker run -v /var/lib/mongo:/data/db --name makechat-mongo -d mongo:latest
    $ docker run -v /etc/makechat.conf:/etc/makechat.conf -v /backups:/backups \
    --name makechat -link mongo-server:makechat-mongo -d makechat:latest
    $ docker run --name makechat-web -d makechat-web:latest

#. Edit ``/etc/makechat.conf``
#. Restart backend::

    $ docker restart makechat
#. Go to ``http://youdomain.com/makechat/admin`` and create user accounts/rooms

#######
Upgrade
#######
Make these steps:

#. Backup **makechat** instance::

    $ docker exec makechat backup

#. Stop **makechat** container and remove it::

    $ docker stop makechat && docker rm makechat

#. Inform users about maintenance::

    $ docker exec makechat-web maintenance on

#. Create new **makechat** container with latest **makechat** package::

    $ docker run -v /etc/makechat.conf:/etc/makechat.conf -v /backups:/backups \
    --name makechat -link mongo-server:makechat-mongo -d makechat:latest

#. Stop maintenance::

    $ docker exec makechat-web maintenance off


