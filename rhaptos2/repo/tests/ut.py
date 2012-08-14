
import unittest
import doctestsupport
import doctest


tsuite = doctest.DocFileSuite('test.txt', checker=doctestsupport.MyOutputChecker())

unittest.TextTestRunner(verbosity=2).run(tsuite)
