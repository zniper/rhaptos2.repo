

set -e

### USAGE
USAGE="bash foo.sh TGTDIR"
## setup as simply but non-destructively teh Rhaptos2 repo
## assumes we are on POSIX and have curl

### We have a script to build a Venv - buildvenv.sh
### This makes no assumptions about hard coded URLS or paths.
### However to be actually user friendly we *do* have to make such assumptions
### so ...

### This script will assume it is in an empty directory and that


function isempty() {
    ###if anything other than$1 is empty exit
    dir=$1

    [ $# -eq 0 ] && { echo "Usage: $USAGE"; exit 2; }
    [ ! -d "$dir" ] && { echo "$dir is not a directory."; exit 2; }

    if find "$dir" -maxdepth 0 -empty | read;
    then
     echo "$dir empty."
    else
     echo "$dir not empty. Please supply an empty target dir."; exit 2;
    fi
}

function download_src(){

    ### This is fantastically brittle but needs to exist to make the
    ### overall easy-to-install process work

    mkdir -p -m 0755 $ABSDIR/src
    mkdir -p -m 0755 $ABSDIR/venvs
    cd $ABSDIR/src
    curl -O https://raw.github.com/Connexions/rhaptos2.repo/master/buildvenv.sh
    git clone https://github.com/Connexions/rhaptos2.repo.git
    git clone https://github.com/Connexions/rhaptos2.common.git
    git clone https://github.com/wysiwhat/Aloha-Editor.git aloha
    cd aloha
    git checkout cnx-master
    cd $ABSDIR

}


function inifile() {
    echo ""
    echo "*****************************"
    echo ""
    echo "You need to change the following parts of the ini file:"
    echo "rhaptos2repo_aloha_staging_dir=$ABSDIR/src/aloha"
    echo "then you can "
    echo "cd $ABSDIR/venvs/vrepo; source bin/activate"
    echo "cd $ABSDIR/src/rhaptos2.repo/rhaptos2/repo;"
    echo "python run.py --debug --config=../../local.ini"
    echo "At this point you should see a runing instance"
}

### main:

TGTDIR=$1
ABSDIR=$( cd $TGTDIR ; pwd -P )
isempty $ABSDIR


echo "I shall now download the sources for RHAPTOS2 REPO and setup a venv for it"
download_src

. $ABSDIR/src/buildvenv.sh $ABSDIR/venvs/vrepo $ABSDIR/src/rhaptos2.common  $ABSDIR/src/rhaptos2.repo

inifile
