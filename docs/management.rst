===================
Management commands
===================

###############
User management
###############

* Print help about available actions::

    $ docker exec makechat makechat user -h
    usage: makechat user [-h] {create,changepass} ...

    positional arguments:
      {create,changepass}
        create             create a new user
        changepass         change user password

    optional arguments:
      -h, --help           show this help message and exit

* Print help about ``user create`` action::

    $ docker exec makechat makechat user create -h
    usage: makechat user create [-h] -u USERNAME -p PASSWORD -e EMAIL [-admin]

    optional arguments:
      -h, --help   show this help message and exit
      -u USERNAME  specify username
      -p PASSWORD  specify password
      -e EMAIL     specify email address
      -admin       is superuser?

* Print help about ``user changepass`` action::

    $ docker exec makechat makechat user changepass -h
    usage: makechat user changepass [-h] -u USERNAME -p NEW PASSWORD

    optional arguments:
      -h, --help       show this help message and exit
      -u USERNAME      specify username
      -p NEW PASSWORD  specify new password

* Add a new user account::

    $ docker exec makechat makechat user create -u test_user -p test_pass -e test@example.com

* Add a new superuser(aka admin) account::

    $ docker exec makechat makechat user create -u admin -p admin_pass -e admin@example.com -admin
