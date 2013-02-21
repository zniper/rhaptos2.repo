=================================
Documenting JSON flow of repo API
=================================


THe below is the output of restrest.py.
It documents HTTP conversations as they occur through 
the python requestsmodule. 

THis is still draft

POST /module/
-------------

::

    Content-Length: 827
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "content": "<h1>In CONGRESS, July 4, 1776.<h1>\n<p>The unanimous Declaratio...
        "id_": "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
        "title": "Introduction"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:09 GMT
    content-length: 996
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": null, 
        "Language": null, 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": null, 
        "Summary": null, 
        "content": "<h1>In CONGRESS, July 4, 1776.<h1>\n<p>The unanimous Declaratio...
        "date_created_utc": "2013-02-21T15:10:09.010619", 
        "date_lastmodified_utc": null, 
        "id_": "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
        "subtype": null, 
        "title": "Introduction"
    }


POST /folder/
-------------

::

    Content-Length: 401
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
            "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b", 
            "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6", 
            "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae", 
            "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389", 
            "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8"
        ], 
        "id_": "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707", 
        "title": "Declaration Folder"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:13 GMT
    content-length: 482
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
            "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b", 
            "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6", 
            "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae", 
            "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389", 
            "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8"
        ], 
        "date_created_utc": "2013-02-21T15:10:13.384189", 
        "date_lastmodified_utc": null, 
        "id_": "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707", 
        "title": "Declaration Folder"
    }


POST /collection/
-----------------

::

    Content-Length: 771
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": [
            "Life", 
            "Liberty", 
            "Happiness"
        ], 
        "Language": "English", 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": [
            "Social Sciences"
        ], 
        "Summary": "No.", 
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
            "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b", 
            "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6", 
            "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae", 
            "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389", 
            "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8"
        ], 
        "id_": "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7", 
        "subtype": "Other Report", 
        "title": "United States Declaration Of Independance"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:18 GMT
    content-length: 852
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": [
            "Life", 
            "Liberty", 
            "Happiness"
        ], 
        "Language": "English", 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": [
            "Social Sciences"
        ], 
        "Summary": "No.", 
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
            "cnxmodule:350f7859-e6e7-11e1-928f-2c768ae4951b", 
            "cnxmodule:4ba18842-1bf8-485b-a6c3-f6e15dd762f6", 
            "cnxmodule:77a45e48-6e91-4814-9cca-0f28348a4aae", 
            "cnxmodule:e0c3cfeb-f2f2-41a0-8c3b-665d79b09389", 
            "cnxmodule:c0b149ec-8dd3-4978-9913-ac87c2770de8"
        ], 
        "date_created_utc": "2013-02-21T15:10:17.964797", 
        "date_lastmodified_utc": null, 
        "id_": "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7", 
        "subtype": "Other Report", 
        "title": "United States Declaration Of Independance"
    }


PUT /module/cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126/
-----------------------------------------------------------

::

    Content-Length: 322
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "content": "Dear King George, cup of tea?", 
        "id_": "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
        "title": "Introduction"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:30 GMT
    content-length: 491
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": null, 
        "Language": null, 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": null, 
        "Summary": null, 
        "content": "Dear King George, cup of tea?", 
        "date_created_utc": "2013-02-21T15:10:09.010619", 
        "date_lastmodified_utc": null, 
        "id_": "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126", 
        "subtype": null, 
        "title": "Introduction"
    }


PUT /collection/cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7/
-------------------------------------------------------------------

::

    Content-Length: 521
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": [
            "Life", 
            "Liberty", 
            "Happiness"
        ], 
        "Language": "English", 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": [
            "Social Sciences"
        ], 
        "Summary": "No.", 
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
        ], 
        "id_": "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7", 
        "subtype": "Other Report", 
        "title": "United States Declaration Of Independance"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:35 GMT
    content-length: 602
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "Authors": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "CopyrightHolders": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Keywords": [
            "Life", 
            "Liberty", 
            "Happiness"
        ], 
        "Language": "English", 
        "Maintainers": [
            "cnxuser:f9647df6-cc6e-4885-9b53-254aa55a3383"
        ], 
        "Subjects": [
            "Social Sciences"
        ], 
        "Summary": "No.", 
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
        ], 
        "date_created_utc": "2013-02-21T15:10:17.964797", 
        "date_lastmodified_utc": null, 
        "id_": "cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7", 
        "subtype": "Other Report", 
        "title": "United States Declaration Of Independance"
    }


PUT /folder/cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707/
-----------------------------------------------------------

::

    Content-Length: 151
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    Accept: */*
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...
    content-type: application/json


Body::

    {
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
        ], 
        "id_": "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707", 
        "title": "Declaration Folder"
    }


Response:: 

    date: Thu, 21 Feb 2013 15:10:42 GMT
    content-length: 232
    content-type: application/json
    server: Werkzeug/0.8.3 Python/2.7.3


::

    {
        "content": [
            "cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126"
        ], 
        "date_created_utc": "2013-02-21T15:10:13.384189", 
        "date_lastmodified_utc": null, 
        "id_": "cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707", 
        "title": "Declaration Folder"
    }


DELETE /folder/cnxfolder:c192bcaf-669a-44c5-b799-96ae00ef4707/
--------------------------------------------------------------

::

    Accept: */*
    Content-Length: 0
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...


Response:: 

    date: Thu, 21 Feb 2013 15:11:01 GMT
    content-length: 0
    content-type: text/html; charset=utf-8
    server: Werkzeug/0.8.3 Python/2.7.3


::

    ...


DELETE /collection/cnxcollection:be7790d1-9ee4-4b25-be84-30b7208f5db7/
----------------------------------------------------------------------

::

    Accept: */*
    Content-Length: 0
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...


Response:: 

    date: Thu, 21 Feb 2013 15:11:07 GMT
    content-length: 0
    content-type: text/html; charset=utf-8
    server: Werkzeug/0.8.3 Python/2.7.3


::

    ...


DELETE /module/cnxmodule:d3911c28-2a9e-4153-9546-f71d83e41126/
--------------------------------------------------------------

::

    Accept: */*
    Content-Length: 0
    Accept-Encoding: gzip, deflate, compress
    X-Cnx-FakeUserId: cnxuser:1234
    User-Agent: python-requests/1.1.0 CPython/2.7.3 Free...


Response:: 

    date: Thu, 21 Feb 2013 15:11:27 GMT
    content-length: 0
    content-type: text/html; charset=utf-8
    server: Werkzeug/0.8.3 Python/2.7.3


::

    ...


