#!/usr/bin/env python3

from setuptools import setup

with open('requirements.txt', 'r') as f:
    install_reqs = [
        s for s in [
            line.strip(' \n') for line in f
        ] if not s.startswith('#') and s != ''
    ]

setup(
    name='ugesco',
    version='0.3',
    packages=['ugfunctions'],
    url='https://github.com/ulbstic/ugescovalidator',
    license='MIT',
    author='Ettore Rizza',
    author_email='erizza@ulb.ac.be',
    description='clustering and disambiguisation of a list of place names',
    python_requires='>=3.5',
    install_requires=install_reqs
)
