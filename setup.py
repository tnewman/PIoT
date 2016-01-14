#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='PIoT',
    description='Internet of Things Platform for Raspberry PI',
    version='0.1dev',
    packages=['piot',],
    license='MIT',
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'python-periphery',
        'sqlalchemy',
        'twilio',
    ],
    tests_require=[
        'pytest',
    ],
)
