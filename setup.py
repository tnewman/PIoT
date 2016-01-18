#!/usr/bin/env python3

from setuptools import setup

setup(
    name='PIoT',
    description='Internet of Things Platform for Raspberry PI',
    version='0.1.dev0',
    packages=['piot',],
    license='MIT',
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'python-periphery',
        'schedule',
        'sqlalchemy',
        'twilio',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
)
