==============
helper scripts
==============

I have developed several helper scripts


* build_local.sh

  will run the complete local stage, build and deploy to remote servers, of the 
  current working tree.  This is almost the same as used by jenkins, but 
  uses a flag to tell staging process (local build and config) to just
  :cmd:`cp -r` not :cmd:`git clone`

* stage_local.sh
  
  As above but only does local staging.  Useful to have a staged area to 
  indivudally run fab files, or other checks.  Could be a flag out of 
  :file:`build_local.sh`

* update_venv.sh

  create a venv in HOMEDIR/venvs/$1
  rebuilod rhaptos2 and pip install in the venv.

  Useful for docs. occassional testing.



  
