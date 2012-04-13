#!/usr/local/bin/python

'''
:author: pbrian <paul@mikadosoftware.com>

This is a demo of Selenium test for tinyMCE.  Only problem is its not working, so I am giving up right now and will come back to it
'''

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("http://localhost/tinydemo.html")

print 'slleping'
import time
time.sleep(5)

print 'find elem'
#driver.type("dom=document.getElementById('tiny1').contentDocument.body", 'ffff')
inputElement = driver.find_element_by_id('content_ifr')
print 'sendkeys'

# type in the search
inputElement.send_keys("Cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

# the page is ajaxy so the title is originally this:
print driver.title

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith("cheese!"))

    # You should see "cheese! - Google Search"
    print driver.title

finally:
    driver.quit()
