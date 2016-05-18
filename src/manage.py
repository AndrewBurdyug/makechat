#!/usr/bin/env python
"""Simple makechat manager."""
import argparse
from mongoengine.errors import NotUniqueError, ValidationError

from makechat.api import run_server
from makechat.api.utils import encrypt_password
from makechat.models import User

parser = argparse.ArgumentParser(description='makechat parser')
subparsers = parser.add_subparsers(dest='mode')
server = subparsers.add_parser('backend', help='backend management')
user = subparsers.add_parser('user', help='user management')
user_subparsers = user.add_subparsers(dest='operation')
server_subparsers = server.add_subparsers(dest='operation')

server_run = server_subparsers.add_parser('run', help='run the backend app')
server_run.add_argument('-p', metavar='PORT', dest='port',
                        help='listen on port', type=int, default=8000)

create_user = user_subparsers.add_parser('create',
                                         help='create a new user')
create_user.add_argument('-u', metavar='USERNAME', dest='username',
                         help='specify username', required=True, type=str)
create_user.add_argument('-p', metavar='PASSWORD', dest='password',
                         help='specify password', required=True, type=str)
create_user.add_argument('-e', metavar='EMAIL', dest='email',
                         help='specify email address', required=True, type=str)
create_user.add_argument('-admin', dest='admin', default=False,
                         help='is superuser?', action='store_true')

change_pass = user_subparsers.add_parser('changepass',
                                         help='change user password')
change_pass.add_argument('-u', metavar='USERNAME', dest='username',
                         help='specify username', required=True, type=str)
change_pass.add_argument('-p', metavar='NEW PASSWORD', dest='password',
                         help='specify new password', required=True, type=str)


def main():
    """Main program: parse the commands and run."""
    args = parser.parse_args()

    if args.mode == 'backend':
        # run backend app
        if args.operation == 'run':
            run_server(args.port)

    if args.mode == 'user':
        # crete a new user
        if args.operation == 'create':
            try:
                User.objects.create(
                    username=args.username,
                    password=encrypt_password(args.password),
                    email=args.email,
                    is_superuser=args.admin)
            except (ValidationError, NotUniqueError) as er:
                print('ERROR:', er)
                exit(1)
        # change password of existing user
        if args.operation == 'changepass':
            try:
                user = User.objects.get(username=args.username)
            except User.DoesNotExist:
                print('ERROR: user does not exist')
                exit(1)
            else:
                user.update(password=encrypt_password(args.password))
