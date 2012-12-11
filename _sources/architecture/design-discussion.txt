==================
Design discussions
==================

This is a page for noting design / architecture issues and noting the
pros and cons of variopus solutions.  Overtime it should become a why
we did what we did resource.

Same Origin Policy
==================

We intend to use AJAX for a large majority of the work we do. AJAX has
a severe limitation, called the `Same Origin Policy
<http://en.wikipedia.org/wiki/Same_origin_policy>`_.

In short, a web page loaded from server x.y.z is prevented by the
browser from *recieving a response*> from server a.y.z (Yes AJAX can
send a request, the other server will return it - all visible through
something like Charles, what wont happen is the response be available
in the browser.)

I am temproarily getting around this using `CORS
<http://en.wikipedia.org/wiki/Cross-Origin_Resource_Sharing>`_ but
this will not support the majority of browsers, so a different
solution is needed.  JSONP only supports GET, so it is not a perfect
fix.

In general proxying requests is the only solution, usually via a
proxy-rewrite, but that is complex to maintain during initial
development so I am leaving it for later pain.

Logging and debugging
=====================

http://www.drdobbs.com/article/print?articleID=196802787&dept_url=/dept/debug/

Todo: Setup centralised logging server


Client side application 
=======================

http://lucumr.pocoo.org/2011/11/15/modern-web-applications-are-here/
http://lucumr.pocoo.org/2011/7/27/the-pluggable-pipedream/

