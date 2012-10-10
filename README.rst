.. Paul Brian, Michael Mulich, (C) 2012 Rice University

   This software is subject to the provisions of the GNU Lesser General
   Public License Version 2.1 (LGPL).  See LICENSE.txt for details.

=============
rhaptos2.repo
=============

This is the repository for Connexions editor.  It is designed to work
primarily as a web application in conjunction with multiple other systems
deployed using the bamboo setup files.

See the `Connexions development documentation
<http://connexions.github.com/>`_ for more information.

Install
-------

The following will setup a development install. For instructions about
a production deployment, go to http://connexions.github.com/ .

Pre-requisites

     Python 2.7 (with header files)
     Bash >=4.0      (system dependant)
     Internet access (!)

All other python level dependencies are taken care of in the
package's `setup.py`. 

.. note:: It is recommended that you do the installation in a
   `virtual environment <http://pypi.python.org/pypi/virtualenv>`_.



To install, run something similar to the following.

Start by checking out the code to your local machine::

    git clone <url>

You may also need to checkout and install the in-development
dependencies:

:rhaptos2.common: https://github.com/Connexions/rhaptos2.common

Install the package by running its `setup.py`::

    cd rhaptos2.repo
    python setup.py develop

This will have installed the code into the Python environment as well
as a script that will run the repository.

Run the application
-------------------

To run the application. You will need to set some environment
variables. ( I'm punting here because I don't know what the environment
variables are. :P ) Then you can run the script that comes with the
application with debug-mode enabled::

    rhaptos2_runrepo --debug=on

The address that the application is running at will be shown in the
first few lines of output. By default this is http://127.0.0.1:5000/.
