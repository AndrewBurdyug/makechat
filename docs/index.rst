========
Overview
========

###################
Introduction
###################
There are many chat programs, but almost all of them have the same
disadvantages:

* not open source, possible have many hidden bugs/leaks
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

#######
Upgrade
#######
Make these steps:

#. Backup **makechat** instance::

    $ docker exec makechat backup

#. Inform users about maintenance::

    $ docker exec makechat-web maintenance on

#. Update docker images::

    $ docker pull buran/makechat
    $ docker pull buran/makechat-web

#. Stop **makechat-web** container and remove it:

    .. code-block:: sh

        $ docker stop makechat-web && docker rm makechat-web

    .. note::

        Usually you do not to worry about downtime of frontend, because time of creation
        new makechat-web instance ~2-5 seconds, so your users may noticed only small lags.
        But if you want to enable maintenance page for a time of update **makechat-web**,
        you should use **makechat-web** behind frontend web server(Nginx/Apache etc) and
        make appropriate changes to its configuration. For example, if you have Nginx
        as frontend web server for **makechat-web** docker instance, you should make
        something like this:

        .. code-block:: nginx

            server {
                listen 80;
                server_name mymakechat.com;
                error_page 503 /maintenance.html;

                location / {
                    return 503;
                }

                location = /maintenance.html {
                    root /path/to/maintenance.html;
                    internal;
                }
            }

#. Create new **makechat-web** container with latest public content and nginx configuration::

    $ docker run --net=makechat_nw --ip=172.30.1.3 --name makechat-web \
        -v /var/www/makechat:/usr/share/nginx/html/makechat/custom \
        -d buran/makechat-web:latest

#. Stop **makechat** container and remove it::

    $ docker stop makechat && docker rm makechat

#. Create new **makechat** container with latest **makechat** package::

    $ docker run --net=makechat_nw --ip=172.30.1.2 -v /makechat-backups:/backups \
        --name makechat -d buran/makechat:latest

#. Stop maintenance::

    $ docker exec makechat-web maintenance off


###############
User management
###############

* Print help about available actions::

    $ docker exec makechat makechat user -h
    usage: manage.py user [-h] {create,changepass} ...

    positional arguments:
      {create,changepass}
        create             create a new user
        changepass         change user password

    optional arguments:
      -h, --help           show this help message and exit

* Print help about ``user create`` action::

    $ docker exec makechat makechat user create -h
    usage: manage.py user create [-h] -u USERNAME -p PASSWORD -e EMAIL [-admin]

    optional arguments:
      -h, --help   show this help message and exit
      -u USERNAME  specify username
      -p PASSWORD  specify password
      -e EMAIL     specify email address
      -admin       is superuser?

* Print help about ``user changepass`` action::

    $ docker exec makechat makechat changepass -h
    usage: manage.py user changepass [-h] -u USERNAME -p NEW PASSWORD

    optional arguments:
      -h, --help       show this help message and exit
      -u USERNAME      specify username
      -p NEW PASSWORD  specify new password

* Add a new user account::

    $ docker exec makechat makechat user create -u test_user -p test_pass -e test@example.com

* Add a new superuser(aka admin) account::

    $ docker exec makechat makechat user create -u admin -p admin_pass -e admin@example.com -admin

