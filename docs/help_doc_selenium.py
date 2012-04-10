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



