#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


'''
setup.py for rhaptos2

'''

from distutils.core import setup
import os, glob

def get_version():

    '''return version from fixed always must exist file

       Making very broad assumptions about the 
       existence of files '''
    
    v = open('rhaptos2/repo/version.txt').read().strip()
    return v




def main():

    setup(name='rhaptos2.repo',
          version=get_version(),
          packages=['rhaptos2.repo'
                    ,'rhaptos2.client'
                   ],
          namespace_packages = ['rhaptos2'],
          author='See AUTHORS.txt',
          author_email='info@cnx.org',
          url='https://github.com/Connexions/rhaptos2.repo',
          license='LICENSE.txt',
          description='New editor / repo / system for cnx.org -rhaptos2.readthedocs.org',
          long_description='see description',
          install_requires=[
              "fabric >= 1.0.0"
              ,"flask >= 0.8"
              ,"statsd"
              ,"requests"
              ,"pylint"
              ,"Flask-OpenID"
              ,"python-memcached"
              ,"nose"

              ,"rhaptos2.common >= 0.0.12"
              ,"unittest-xml-reporting"
              ,"mikado.oss.doctest_additions"
              ,"python-memcached"
                           ],
          scripts=glob.glob('scripts/*'),

          package_data={'rhaptos2.repo': ['templates/*.*', 
                                          'static/*.*', 
                                           'version.txt', 
                                           'tests/*.*'],
                        },

          
          )



if __name__ == '__main__':
    main()

