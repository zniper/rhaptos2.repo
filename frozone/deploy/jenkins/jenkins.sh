git pull
make stage localgitrepo=/tmp/clone/frozone localstage=/tmp/staging configfile=office_conf.py host=devjenkins fabfile=deploy/fab_stage.py

export PYTHONPATH=/tmp/staging && make clean-remote host=devweb fabfile=deploy/fab_app_frozone.p
export PYTHONPATH=/tmp/staging && make remote-install-e2repo host=devweb fabfile=deploy/fab_app_frozone.py
export PYTHONPATH=/tmp/staging && make remote-install-cdn host=devweb fabfile=deploy/fab_app_frozone.py
start supervisor

