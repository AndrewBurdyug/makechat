"""Makechat package.

Project URL:
Documentations URL:

"""
from setuptools import setup

setup(
    name="makechat",
    version="0.1.3",
    packages=['makechat'],
    install_requires=[
        'cython>=0.23.4',
        'falcon==0.3.0',
        'mongoengine==0.10.6',
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
