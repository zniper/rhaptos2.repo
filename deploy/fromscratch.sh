# Will need the lxc setup as described, with usernames esp deployagent

fab -H frozone.mikadosoftware.com -f fab_app_frozone.py local_init
fab -H frozone.mikadosoftware.com -f fab_app_frozone.py local_clone_overwrite
fab -H frozone.mikadosoftware.com -f fab_app_frozone.py remote_init

fab -H frozone.mikadosoftware.com -f fab_app_frozone.py install_cdn

fab -H frozone.mikadosoftware.com -f fab_app_frozone.py install_e2client
fab -H frozone.mikadosoftware.com -f fab_app_frozone.py install_e2client
fab -H frozone.mikadosoftware.com -f fab_app_frozone.py install_supervisor

#Now (re)start supervisord (running non daemon fro testing purposes)

#convert to Makefile asap



