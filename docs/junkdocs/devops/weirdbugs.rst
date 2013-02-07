====
Misc
====

ReadTheDocs: seems to not like modules with _ in the names.
Not sure how they are configuring Sphonx but its an easy workaround


The Flask internal webserver is HTTP/1.0 only, which after three hours I finally noticed, and solved the ajax problems

JQuery - broken pipes on AJAX calls.  usually this is because the browser, which sends off an AJAX request, then breaks that connection.  Usually this is because the browser has fired the ajax call off a <a> link, and then carried on with the action the link has - that is to move to a new page.  So the entire running code on the page (incl the bit waiting for a reply from server) gets garbage collected, the server has its socket killed, broken pipe.  The fix
- to add event.preventDefault()  - see John Resig tutorial.


This is such a common issue we need to build in solutions.  Assume it will always happen.  Use httplib and do a good test too.

* ImportError: No module named site
  Caused by trying to run (uwsgi) in a virtualenv when there is not one.
  --home arg is not what it said :-)

* http://lists.unbit.it/pipermail/uwsgi/2010-March/000188.html
  invalid request block size: 21573

  ET as little endian is 21573, but GET sent by HTTP *to* a wsgi server is going to be funny - cos wsgi servers are not http servers...


* when booting a container (seemingly the last numbered/built container)
  it's netowkr stack does not come up.  You need to login to console
  (lxc-console -n cnx4) and just ping anywhere.
  I have modified rc.local to ping -c 3 www.google.com just to acheive thois

