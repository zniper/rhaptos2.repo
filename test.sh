

#1. go to a clone of git
#2. git pull on the right branch
#3. make stage

cd /home/pbrian/jenkinstest/frozone

git pull

make stage localgitrepo=./ \
              localstage=/tmp/staging/frozone \
              configfile=conf.d/frozone.ini \
              host=localhost \
              fabfile=deploy/fab_stage.py

cd /tmp/staging/frozone
make clean-remote host=devweb \
                        fabfile=deploy/fab_app_frozone.py \
                        localstagingdir=/tmp/staging/frozone

make remote-install-cdn host=devweb \
                        fabfile=deploy/fab_app_frozone.py \
                        localstagingdir=/tmp/staging/frozone


make remote-install-e2repo host=devweb \
                        fabfile=deploy/fab_app_frozone.py \
                        localstagingdir=/tmp/staging/frozone


