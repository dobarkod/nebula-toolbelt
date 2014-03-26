#!/usr/bin/env python
import os
import sys

from setuptools import setup


VERSION = '0.0.2'


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
    url='https://github.com/dobarkod/nebula-toolbelt',
    packages=['nebula'],
    license='Apache 2.0',
    scripts=scripts,
    install_requires=['docopt >= 0.6.1', 'requests >= 2.0.1'],
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
