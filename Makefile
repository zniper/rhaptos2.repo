
### Simple message.
TBC='Not yet implemented - see frozone.readthedocs.org'

clean: clean-crud

clean-crud:
	find ./ -name "*.pyc" -type f -exec rm {} \;
	find ./ -name "*.py~" -type f -exec rm {} \;

clean-local:
	fab -H $(host) -f $(fabfile) clean_local
#make stage localgitrepo=/tmp/clone localstage=/tmp/staging configfile=office_conf.py \
host=devjenkins fabfile=deploy/fab_stage.py
stage:
	fab -H $(host) -f $(fabfile) stage:localgitrepo=$(localgitrepo),localstage=$(localstage),configfile=$(configfile)



clean-remote:
	fab -H $(host) -f $(fabfile) remote_init


remote-install-cdn:
	fab -H $(host) -f $(fabfile) install_cdn

remote-install-e2repo:
	fab -H $(host) -f $(fabfile) install_www
	fab -H $(host) -f $(fabfile) install_supervisor

remote-install-e2server:
	echo $(TBC)

remote-start-supervisor:
	echo $(TBC)


# make newcontainer host=hpcube fabfile=deploy/fab_lxc.py vhostname=dev1 vhostip=10.0.0.21
newcontainer:
	fab -H $(host) -f $(fabfile) build_new_container:vhostname=$(vhostname),vhostip=$(vhostip)
	fab -H $(host) -f $(fabfile) preboot:vhostname=$(vhostname),vhostip=$(vhostip)
	fab -H $(vhostname) -f $(fabfile) useradd:username=deployagent,passwd=deployagent
	fab -H $(vhostname) -f $(fabfile) postboot

# make lxc-destroy host=hpcube fabfile=deploy/fab_lxc.py vhostname=dev1 vhostip=10.0.0.21
lxc_destroy:
	fab -H $(host) -f $(fabfile) lxc_destroy:vhostname=$(vhostname)

# make jenkins host=devjenkins fabfile=deploy/fab_sys_jenkins.py 
jenkins:
	fab -H $(host) -f $(fabfile) install_jenkins

# make graphite host=devlog fabfile=deploy/fab_sys_graphite.py 
# NB this assumes the statsd and graphite are on same host...
graphite: 
	fab -H $(host) -f $(fabfile) install_graphite_deps
	fab -H $(host) -f $(fabfile) install_graphite
	fab -H $(host) -f $(fabfile) install_statsd:graphitehost=$(host)

# make repo host=devweb fabfile=deploy/fab_sys_repo.py
repo:
	fab -H $(host) -f $(fabfile) prepare_repo