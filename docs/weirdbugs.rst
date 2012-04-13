

ReadTheDocs: seems to not like modules with _ in the names.
Not sure how they are configuring Sphonx but its an easy workaround


The Flask internal webserver is HTTP/1.0 only, which after three hours I finally noticed, and solved the ajax problems

JQuery - broken pipes on AJAX calls.  usually this is because the browser, which sends off an AJAX request, then breaks that connection.  Usually this is because the browser has fired the ajax call off a <a> link, and then carried on with the action the link has - that is to move to a new page.  So the entire running code on the page (incl the bit waiting for a reply from server) gets garbage collected, the server has its socket killed, broken pipe.  The fix
- to add event.preventDefault()  - see John Resig tutorial.

