"""Import makechat configuration from /etc/makechat.conf."""

import configparser
import os.path

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/makechat.conf'))
