Welcome to ednamode's documentation!
====================================


Start Here

.. toctree::
   :maxdepth: 2

   overview
   requirements
   development_guidelines
   webservers


Details
-------

.. automodule:: ednamode


e2repo - the repository
=======================

The repository is pretty simple for now - but it needs to be clear about whether
we are aiming for git style unique references for every change to every module,
or if a module is to be a fixed named resource, and we track the versions of the module.
(Begging question when does it stop being a named module...  my gut feeling is take the DVCS / git approach.  But it has issues.

.. automodule:: ednamode.e2repo.repolib
   :members:



   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

