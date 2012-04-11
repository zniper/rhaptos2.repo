Web servers
===========


A side note on HTTP, REST and PUT/DELETE
----------------------------------------

Forgive me if this is old news to everyone but I wanted to get it as
straight as possible.

HTTP the protocol has 4 main 'request methods' - GET POST PUT DELETE (see `here <http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods>`_).

HTML Forms however are limited to just supporting GET and POST. (see )

Now, TinyMCE is a POST style browser.  Often we dont want to tunnel PUT / DELETE through POST browsers.

Our options are 

1. end run tiny, and get Jquery to actually do the request over XMLHTTPREQUEST
2. errr...

So I have two solutions, ready 

1. a wsgi wrapper that will look for and fix tunnel'd calls
   It should conform as much as possible to the same thing done for django 
2. a test suite showing how Flask responds to the diff HTTP request types. 


Creating a WSGI wrapper in Flask
--------------------------------

We want to be able to handle two kinds of HTTP request.

1. Genuine - a HTTP header is sent correctly
2. Tunneled - we use some flag in POST request and convert to that flag before processing on server.  See flask_POST_tunnel


