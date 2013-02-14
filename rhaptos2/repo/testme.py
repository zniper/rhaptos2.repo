import doctest

doctest.testfile("example.txt",
                 optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

doctest.testfile("coltest.txt",
                 optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

doctest.testfile("modtest.txt",
                 optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)
