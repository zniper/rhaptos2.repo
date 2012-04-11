Welcome to ednamode's documentation!
====================================


Start Here

.. toctree::
   :maxdepth: 2

   overview
   requirements
   development_guidelines
   webservers


e2server - server
=================

The server is for now a bit experimental - again we have some fundamental but difficult design decisions.
Perhaps it is ripe time to experiment - write something, put under heavy load.

Anyway. 

We want to run Flask.  Behind a solid webserver like nginx. So I have chosen to use the `uWSGI <projects.unbit.it/uwsgi/>`_
application server.  The set up for this is to be put into the install files. 

Testing this server - as noted in the webserver notes above, 


Current setup - I am running on the so-called development laptop (!) hadrian. 
I have the server there, and the other development laptop is running firefox with the `Charles <http://www.charlesproxy.com>`_ proxy.
I recommend this - its worth the 30 bucks or so.  Especially watching the raw forms.


.. automodule:: e2server.flask_POST_tunnel


Here I am attaching my own middleware to the wsgi flow - it will look for a trigger 
element in the form, and then replace the POST method in the CGI environ variables with 
the methid in the trigger - ie. we POST a form that says trigger=DELETE and then 
this before any new processing is done, flips the environ to be DELETE.

THis is only useful for non-AJAX mediated calls - its a hedge against having problems with tinyMCE

I will write it up a bit and then leave it


e2repo - the repository
=======================

The repository is pretty simple for now - but it needs to be clear about whether
we are aiming for git style unique references for every change to every module,
or if a module is to be a fixed named resource, and we track the versions of the module.
(Begging question when does it stop being a named module...  my gut feeling is take the DVCS / git approach.  But it has issues.

.. automodule:: e2repo.repolib
   :members:



   


