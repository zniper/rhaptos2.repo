#make host=cnx1	fabfile=deploy/fab_app_frozone.py branch=screamingmess	context=office stageonly
cd _config
python mother_of_all_conf.py
cd ..
make host=cnx1	fabfile=deploy/fab_app_frozone.py branch=convertToOneRepoNoServer context=office oneinstall

