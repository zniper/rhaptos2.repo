#!/usr/local/bin/bash

set -e
#set -u

# assuming we have a venv at ~/venvs/dev
# assuming we want to regularly and frequently test a pyhton pkg
# keep the env up

### run staging first
cd ~/cnx/bamboo
. deploy.sh stage -- ~/cnx

VENVROOT=~

### expand these tests to ensure valid env
### Needs a venvname
if test -z "$1"
then
  echo "Must supply a Virtualenv name that will be $1/xxx"
  exit 1
fi



VENVNAME=$1

ENVPATH=$VENVROOT/$VENVNAME
ENVPYTHON=$ENVPATH/bin/python
ENVPIP=$ENVPATH/bin/pip
SETUP=$LOCALSTAGEROOT/rhaptos2.repo/setup.py

#######
echo "########## update env sanity check"
echo ENVPATH = $ENVPATH
echo ENVPYTHON = $ENVPYTHON
echo ENVPIP = $ENVPIP
echo SETUP = $SETUP



### sanity check
if [ -f $SETUP ]
then
    echo "Found a rhaptos2 -  Proceeding"
else
    echo "Bamboo Error: Sorry, no setup.py at $SETUP."
    exit
fi




function initial_venv_creation() {

 mkdir -p -m 0777 $VENVROOT

 cd $VENVROOT
 virtualenv $VENVNAME
 
}

# function reinstall_pysqlite(){

#   ## pysqlite refuses to build when pip bulds it - it needs to be built staticvally.
#   ## catch the error of building pysqlite in trap, sendit up here, and continue.

#   cd $ENVPATH/build/pysqlite && $ENVPYTHON setup.py build_static install
#   create_install_new_rhaptos2_pkg
#   ##exit
#   ## explicitly carry on.. hmmm
# }


function create_install_new_rhaptos2_pkg() {


#    trap reinstall_pysqlite ERR


    echo ">>> Starting pkg compile for rhaptos2"
    echo $LOCALSTAGEROOT


    ## uninstall rhaptos from venv, ignore if its not already installed
    
    yes y | $ENVPIP uninstall rhaptos2 || true
    

    #create a new dist pkg
    cd $LOCALSTAGEROOT/rhaptos2.repo
    rm -rf dist/
    $ENVPYTHON $SETUP sdist

    $ENVPIP install $LOCALSTAGEROOT/rhaptos2.repo/dist/rhaptos2.repo-*


}




if [ -f $ENVPYTHON ]
then

    echo 'venv exists, just install pkg'
    create_install_new_rhaptos2_pkg
        
else

    echo 'Not found $ENVPYTHON, so assuming no venv created.  Making...'
    initial_venv_creation
    echo 'install new rhaptos to venv'
    create_install_new_rhaptos2_pkg
    
fi






