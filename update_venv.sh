

# assuming we have a venv at ~/venvs/dev
# assuming we want to regularly and frequently test a pyhton pkg
# keep the env up

ENV=/home/pbrian/venvs/dev
ENVPYTHON=$ENV/bin/python
ENVPIP=$ENV/bin/pip
PROJECT=/home/pbrian/frozone/Rhaptos2
SETUP=$PROJECT/setup.py

#create a new dist pkg
cd $PROJECT
$ENVPYTHON $SETUP sdist
yes y | $ENVPIP uninstall rhaptos2
$ENVPIP install $PROJECT/dist/*.gz

