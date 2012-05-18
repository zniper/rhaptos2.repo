
from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.directory = '/tmp/staging/frozone/venv'
env.activate = 'source /tmp/staging/frozone/venv/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def do_replace():
    with virtualenv():
        run('pip freeze')

