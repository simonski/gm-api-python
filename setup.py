#!/usr/bin/env python
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

from gmapi import constants
setup(
    name='gmapi',
    test_suite='tests',
    version=constants.VERSION,
    description='Python bindings to Graymeta.com Platform API v.21+',
    long_description=long_description,
    url='https://github.com/simonski/gm-api-python',
    author='Simon Gauld',
    license='Apache 2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='Client API to Graymeta v.21',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'gm=gmapi.code:main',
        ],
    },
)
