
### Simple message.
TBC='Not yet implemented - see frozone.readthedocs.org'

### config provided from a central config server
include conf.mk

###########
#
# CLEAN
#
#
#
#
#
#
###########

clean: clean-crud

clean-crud:
	find ./ -name "*.pyc" -type f -exec rm {} \;
	find ./ -name "*.py~" -type f -exec rm {} \;

clean-local:
	fab -H $(host) -f $(fabfile) clean_local

stage-local:
	fab -H $(host) -f $(fabfile) stage_local:remote_git_repo=$(remote_git_repo),localgit=$(localgit),localstaging=$(localstaging),branch=$(branch),context=$(context)



clean-remote:
	fab -H $(host) -f $(fabfile) remote_init


remote-install-cdn:
	fab -H $(host) -f $(fabfile) install_cdn

remote-install-e2repo:
	fab -H $(host) -f $(fabfile) install_www
	fab -H $(host) -f $(fabfile) install_supervisor
	echo 'Now run supervisor - sudo supervisord -n -c /home/deployagent/supervisor/supervisord.conf'

remote-install-e2server:
	echo $(TBC)

remote-start-supervisor:
	echo $(TBC)

#make host=cnx1 fabfile=deploy/fab_app_frozone.py branch=master context=office

oneinstall: clean-local stage-local clean-remote remote-install-cdn remote-install-e2repo

stageonly: clean-local stage-local 


# make newcontainer host=hpcube fabfile=deploy/fab_lxc.py vhostname=dev1 vhostip=10.0.0.21
newcontainer:
	fab -H $(host) -f $(fabfile) build_new_container:vhostname=$(vhostname),vhostip=$(vhostip)
	fab -H $(host) -f $(fabfile) preboot:vhostname=$(vhostname),vhostip=$(vhostip)
	fab -H $(vhostname) -f $(fabfile) useradd:username=deployagent,passwd=deployagent
	fab -H $(vhostname) -f $(fabfile) postboot

lxc_destroy:
	fab -H $(host) -f $(fabfile) lxc_destroy:vhostname=$(vhostname)

# make jenkins host=devjenkins fabfile=deploy/fab_sys_jenkins.py 
jenkins:
	fab -H $(host) -f $(fabfile) install_jenkins