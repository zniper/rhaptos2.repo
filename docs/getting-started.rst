===========================
Getting Started - Developer
===========================


Notes on serving everything via flask


Flask is now configured through several variables in config to serve
static directories on its local disk

::

  export rhaptos2repo_aloha_staging_dir=$bamboo_stage_root/aloha/
  export rhaptos2repo_css_staging_dir=$bamboo_stage_root/css/
  export rhaptos2repo_js_staging_dir=$bamboo_stage_root/js/

Aloha is the approriate one to follow here.
github.com/whysiwhat:Aloha-Editor is cloned and cnx-master branch is followed
This is then either symlinked to $bamboo_stage_root/aloha/ or
will be cp'd there during staging phase of a build

Then a view is adjusted in Flask, pointing /cdn/aloha at that directory.

This is how I would like to do bootstrap and all other thirdparty libraries

However, bootstrap is at tag 2.2.0 and we are using 2.1.0.  We can get the source
but will need to compile *before* a diff and maybe not trust it then.

Similarly we need to identify other thrid party librabries and pull them down 
suring build and adjust views.

This is a slightly longer term project.

For now I shall contine to serve them as was.  ALoha is fixed however.




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


