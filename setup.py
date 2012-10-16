#!/usr/bin/env python
#! -*- coding: utf-8 -*-


""" setup.py - rhaptos2.repo package setup

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from setuptools import setup, find_packages
import os, glob
from bamboo.setuptools_version import versionlib


setup(
    name='rhaptos2.repo',
    version=versionlib.get_version('.'),
    packages=find_packages(),
    namespace_packages=['rhaptos2'],
    author='See AUTHORS.txt',
    author_email='info@cnx.org',
    url='https://github.com/Connexions/rhaptos2.repo',
    license='LICENSE.txt',
    description="New editor / repo / system for cnx.org " \
                "-rhaptos2.readthedocs.org",
    install_requires=[
        "bamboo.setuptools_version", 
        "fabric >= 1.0.0",
        "flask >= 0.8",
        "statsd",
        "requests",
        "pylint",
        "Flask-OpenID",
        "python-memcached",
        "nose",

        "rhaptos2.common >= 0.0.12",
        "unittest-xml-reporting",
        ##"mikado.oss.doctest_additions",
        "python-memcached",
        ],
    package_data={'rhaptos2.repo': ['templates/*.*',
                                    'static/*.*',
                                    'version.txt',
                                    'tests/*.*'],
                  },
    entry_points = """\
[console_scripts]
rhaptos2_runrepo = rhaptos2.repo.run:main
""",
    )

