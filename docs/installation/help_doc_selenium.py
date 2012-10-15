#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


from selenium import webdriver
import types

'''
silly quick script to output the docs from seleniim
'''

driver = webdriver.Firefox()

attrs_methods = dir(driver)

for item in attrs_methods :
    print item

    try:
        x = getattr(driver, item)
        print x.__doc__
    except:
        print type(x)



