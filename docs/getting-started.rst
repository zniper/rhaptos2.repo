===========================
Getting Started - Developer
===========================


Just run the repo locally first of all
======================================


::

  git clone git://github.com/lifeisstillgood/frozone.git ~/

  (should now have ~/frozone/Rhaptos2)

  cd ~/frozone

  bash Rhaptos2/scripts/update_venv.sh

  This should create a virtual env in ~/venvs/dev, and dirs in /tmp
  populate it with the pkg built from rhaptos2 and then run the repo
  locally ..

  start local repo
   * Running on http://127.0.0.1:5000/

  Now connect to http://127.0.0.1:5000/workspace/

  you should get back an empty JSON list. 


Build a developer environment
=============================

I am assuming we have a local, spare, server.  I call mine hpcube.
Because its a cube shaped entry level server, from HP.  

see :doc:`install-os` and :doc:`Installation` .


