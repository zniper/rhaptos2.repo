=======
Testing
=======

We use nose.
We have some conventions

* standalone - should run with just python/rhaptos packages 
* with network
* with selenium


Also
----

Use `interlude <>_`
During development, copy the below into a doctest::

 >>> import interlude; interlude.interact(locals())

now run the doctest, and it drops you into a shell at that line
Just use the shell to develop, check, test etc.  Its using locals() *in* the doctest.  Its really helpful.


:biblio:
http://ivory.idyll.org/articles/nose-intro.html
