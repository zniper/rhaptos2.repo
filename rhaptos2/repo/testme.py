import doctest
doctest.testfile("example.txt",
                 optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)
