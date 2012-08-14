


import unittest
import doctestsupport
import doctest
import sys
import xmlrunner

"""
generally just run as normal doctest with our "ignore loglines" setting
But if called with jenkins as arg, then write out a parseable XML file for it.

"""


def test_doctest(f):
    doctestsupport.testfile(f, checker=doctestsupport.MyOutputChecker())

def asunittest(f):

   tsuite = doctest.DocFileSuite(f, checker=doctestsupport.MyOutputChecker())
   xmlrunner.XMLTestRunner(output="mytest").run(tsuite)

def main():
    testfile="local_tests.txt"
    #todo: should use a list of text files...

    args = sys.argv[1:]
    if args:
        if args[0] == 'jenkins':
            asunittest(testfile)
        else:
            test_doctest(testfile)
    else:
        test_doctest(testfile)
  
if __name__ == '__main__':
    main()



