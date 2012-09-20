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
:author: pbrian <paul@mikadosoftware.com>

This is a demo of Selenium test for tinyMCE.  Only problem is its not working, so I am giving up right now and will come back to it
'''


#from selenium import webdriver
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#import time

def donttest():

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # go to the google home page
    driver.get("http://hadrian/rhaptos2/demostrawman.html")

    print 'sleeping'
    import time
    time.sleep(5)


    #tinymce stores the actual editor in a iframe.  It seems to have a sensible name - append _ifr to id
    driver.switch_to_frame('e2textarea_ifr')
    #the next makes a big assumption about what is active, but by default it will  be when first open
    e = driver.switch_to_active_element() 
    #send in text - however not wiping out first lot ...
    e.send_keys('Cheese Monkeys')

    driver.switch_to_default_content()

    post = driver.find_element_by_id('radio_post').click()
    c1 = driver.find_element_by_id('click1').click()
    #at this point we shoudl POST to e2server



    # the page is ajaxy so the title is originally this:

    response=  driver.find_element_by_id('responsearea').html() 
    assert response.find('Cheese Monkeys') >= 0


