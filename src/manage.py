#!/usr/bin/env python
"""Simple makechat manager."""
import argparse
import os
from makechat.api import run_server


parser = argparse.ArgumentParser(description='makechat parser')
parser.add_argument('run_server', help='Run makechat server')

args = parser.parse_args()

if args.run_server:
    pid = os.fork()
    if pid:
        exit(0)
    else:
        run_server()
