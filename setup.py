"""Makechat package.

Project URL:
Documentations URL:

"""
from setuptools import setup

setup(
    name="makechat",
    version="0.1.1",
    packages=['makechat'],
    install_requires=[
        'docutils>=0.3'
    ],
    package_dir={'makechat': 'src'},
    entry_points={
        'console_scripts': [
            'makechat = makechat.manage:__main__'
        ]
    },
    include_package_data=True,
    author="Andrew Burdyug",
    author_email="buran83@gmail.com",
    description="Simple chat system",
    license="Apache License, Version 2.0",
    keywords="chat",
)
