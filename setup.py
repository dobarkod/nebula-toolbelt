#!/usr/bin/env python
import os
import sys

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
with open('./requirements.txt') as requirements_txt:
    requirements = [line for line in requirements_txt]


VERSION = '0.0.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

scripts = ['nebula/nebula']

setup(
    name='nebula',
    version=VERSION,
    author='Deni Bertovic',
    author_email='deni@kset.org',
    description='CLI/Toolbelt for Nebula',
    url='github.com/dobarkod/nebula-toolbelt',
    packages=['nebula'],
    license='Apache 2.0',
    scripts=scripts,
    install_requires=requirements + test_requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Installation/Setup',
        'Topic :: Utilities'
    ],
)
