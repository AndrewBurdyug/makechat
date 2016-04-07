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
