#!/bin/bash

### example:
## bash buildvenv.sh  ~/venvs/vuser ~/src/rhaptos2.common/ ~/src/rhaptos2.repo
##
##We are providing an (ampty) dir to insert the virtualenv into, and
## a list of packages which we want to exist in that venv, as "setup.py develop"
#### HACK!  setup.py develop seems not to allow namespaced pkgs to mix
#### egg.links (ie develop) and regular installs (ie eggs) THis is why
#### we need to download and install as develop all namespaced
#### packages

set -e


### We expect buildvenv.sh <venvpath> <pkgdir> <pkgdir>
### Convert all args to array, gather length of array
### we assume space as delim, and need "" around params with spaces in.
ARRAY=("${@}")
ELEMS=${#ARRAY[@]}


### If not given at least two options...
if [[ "$ELEMS" -lt 2 ]]; then
    echo "Useage:"
    echo >&2 "buildvenv.sh <venvpath> <pkgdir> <pkgdirs...>"
    exit 1
fi


#### build function -
#### assume requirements.txt exists
function buildv {

    pkgdir=$1  ##set first param to useful name

    reqmts=$pkgdir/requirements.txt


    if [[ -z "$reqmts" ]]; then
        echo >&2 "Need requirements file in pkgdir"
        exit 1
    fi


    cd $venvpath
    . bin/activate

    $venvpath/bin/pip install -r $reqmts

    cd $pkgdir
    $venvpath/bin/python setup.py develop


}



venvpath=${ARRAY[0]}

virtualenv $venvpath

for item in "${ARRAY[@]:1:$ELEMS}"
do
    buildv $item
done
