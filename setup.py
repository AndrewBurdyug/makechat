"""Makechat package.

Project URL: http://makechat.tk
Documentations URL: http://makechat.readthedocs.org/en/latest/

"""
import os.path
from setuptools import setup

setup(
    name='makechat',
    version=open('VERSION').read().strip(),
    packages=['makechat'],
    install_requires=[
        'cython==0.24',
        'falcon==1.0.0',
        'mongoengine==0.10.6',
    ],
    package_dir={'makechat': 'src'},
    entry_points={
        'console_scripts': [
            'makechat=makechat.manage:main'
        ]
    },
    include_package_data=True,
    author='Andrew Burdyug',
    author_email='buran83@gmail.com',
    description='Simple chat system',
    url='http://makechat.tk',
    license='Apache License, Version 2.0',
    keywords='chat',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    data_files=[(os.path.expanduser('~/'), ['makechat.conf'])],
)
