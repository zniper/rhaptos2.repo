cd /home/pbrian/venvs
virtualenv test1
. test1/bin/activate
pip install /usr/home/pbrian/com.mikadosoftware/clients/cnx/frozone/Rhaptos2/dist/Rhaptos2-0.0.1.tar.gz 
mkdir -p -m 0777 /tmp/repo/testuser@cnx.org

python -c 'from rhaptos2.repo import e2repo; e2repo.app.run()'
 
#./test1/lib/python2.7/site-packages/rhaptos2/repo/e2repo.py



