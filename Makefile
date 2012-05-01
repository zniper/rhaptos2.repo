TBC='Not yet implemented - see frozone.readthedocs.org'

all:
	echo $(TBC)


clean-crud:
	find ./ -name "*.pyc" -type f -exec rm {} \;
	find ./ -name "*.py~" -type f -exec rm {} \;


srcdir = /home/deployagent/frozone
TINYMCE_STORE = /usr/home/pbrian/frozone/thirdparty/tinymce
localhome = /tmp/frozone
localgit = $(localhome)/git
localstaging = $(localhome)/staging
remote_git_repo = git://github.com/lifeisstillgood/frozone.git
remotewwwdir = /usr/share/www/nginx/cdn
flaskdir_repo = usr/share/www/flask/e2repo
flaskdir_server = usr/share/www/flask/e2server
remotehome=/home/deployagent



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
