#!/usr/local/bin/bash

# assuming we have a venv at ~/venvs/dev
# assuming we want to regularly and frequently test a pyhton pkg
# keep the env up

HOMEDIR=~
PROJECT=$HOMEDIR/frozone/Rhaptos2

VENVNAME=dev1
ENV=$HOMEDIR/venvs/$VENVNAME
ENVPYTHON=$ENV/bin/python
ENVPIP=$ENV/bin/pip
SETUP=$PROJECT/setup.py


### sanity check
if [ -f $SETUP ]
then
    echo "Found a rhaptos2 -  Proceeding"
else
    echo "Sorry, no setup.py at $SETUP.  Have you configured this script right?"
    exit
fi


function initial_venv_creation() {

 mkdir -p -m 0777 $HOMEDIR/venvs
 mkdir -p -m 0777 /tmp/repo/testuser@cnx.org

 cd $HOMEDIR/venvs
 virtualenv $VENVNAME
 
}


function create_install_new_rhaptos2_pkg() {

    #create a new dist pkg
    cd $PROJECT
    $ENVPYTHON $SETUP sdist
    yes y | $ENVPIP uninstall rhaptos2
    $ENVPIP install $PROJECT/dist/*.gz

}



if [ -f $ENVPYTHON ]
then

    echo 'venv exists, just install pkg'
    create_install_new_rhaptos2_pkg
    echo 'start local repo'
    $ENVPYTHON -c 'from rhaptos2.repo import e2repo; e2repo.app.run()'   
    
else

    echo 'Not found $ENVPYTHON, so assuming no venv created.  Making...'
    initial_venv_creation
    echo 'install new rhaptos to venv'
    create_install_new_rhaptos2_pkg
    echo 'start local repo'
    $ENVPYTHON -c 'from rhaptos2.repo import e2repo; e2repo.app.run()'   
fi





