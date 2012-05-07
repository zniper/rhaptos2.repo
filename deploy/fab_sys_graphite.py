#!/usr/local/bin/python

'''
Fab file to install Graphite and Scribe onto a server

'''

import fabric
import fabpass
from fabric.operations import put, open_shell, prompt
from fabric.api import sudo, run, local
import os

STATSD_HOME = '/home/deployagent/statsd'
GRAPHITE_HOME = '/home/deployagent/graphite'
CARBON_HOME = '/home/deployagent/carbon'
WHISPER_HOME = '/home/deployagent/whisper'


def install_graphite_deps():
    ''' 
    install onto a target LXC (ubuntu) the set of pkgs required by Carbon / Graphite
    Set of requirements from http://graphite.wikidot.com/installation
    See the :code: pkgs variable in this function for complete list.

    '''

    pkgs = [ 'apache2', 'apache2-mpm-worker', 'apache2-utils',
             'apache2.2-bin', 'apache2.2-common', 'libapr1',
             'libaprutil1', 'libaprutil1-dbd-sqlite3', 'libapache2-mod-wsgi',
             'libaprutil1-ldap', 'memcached', 'python-cairo-dev',
             'python-django', 'python-ldap', 'python-memcache',
             'python-pysqlite2', 'sqlite3', 'erlang-os-mon',
             'erlang-snmp', 'rabbitmq-server', 'bzr',
             'expect', 'ssh', 'libapache2-mod-python',
             'python-setuptools', 'python-twisted',
             
           ]

    for pkg in pkgs:
        sudo('apt-get install -y %s' % pkg)

    sudo('easy_install django-tagging')



def install_graphite1():
    ''' Grab the sources, build, then signal how to configure '''

    sh = '''
        apt-get update
        apt-get upgrade
        apt-get install -y wget
        wget http://launchpad.net/graphite/0.9/0.9.9/+download/graphite-web-0.9.9.tar.gz
        wget http://launchpad.net/graphite/0.9/0.9.9/+download/carbon-0.9.9.tar.gz
        wget http://launchpad.net/graphite/0.9/0.9.9/+download/whisper-0.9.9.tar.gz
        tar -zxvf graphite-web-0.9.9.tar.gz
        tar -zxvf carbon-0.9.9.tar.gz
        tar -zxvf whisper-0.9.9.tar.gz
        mv graphite-web-0.9.9 graphite
        mv carbon-0.9.9 carbon
        mv whisper-0.9.9 whisper
        rm carbon-0.9.9.tar.gz
        rm graphite-web-0.9.9.tar.gz
        rm whisper-0.9.9.tar.gz
        '''

    for line in sh.split('\n'):
        cmd = line.strip()
        sudo(cmd)

    prompt('install whisper Y?','OK')

    with fabric.context_managers.cd('/home/deployagent/whisper'):
        sudo('python setup.py install')

    prompt('install carbon Y?','OK')

    with fabric.context_managers.cd('/home/deployagent/carbon'):
        sudo('python setup.py install')

    with fabric.context_managers.cd('/opt/graphite/conf'):
        sudo('cp carbon.conf.example carbon.conf')
        #sudo('cp storage-schemas.conf.example storage-schemas.conf')
        sudo('''cat > storage-schemas.conf << EOF
[stats]
priority = 110
pattern = .*
retentions = 10:2160,60:10080,600:262974
EOF
''')

     
    prompt('I will now run the graphite dependency check, Ctl-C if a problem - Y=cont.')
    sudo('cd /home/deployagent/graphite/ && python check-dependencies.py')
    prompt('Was the check ok? Ent to cont. Ctl-C abort.')
    sudo('cd /home/deployagent/graphite && python setup.py install')


#configure apache

    with fabric.context_managers.cd('/home/deployagent/graphite/examples'):
        sudo('cp example-graphite-vhost.conf /etc/apache2/sites-available/default')
        sudo('cp /opt/graphite/conf/graphite.wsgi.example /opt/graphite/conf/graphite.wsgi')
        sudo('mkdir -p -m 0777 /etc/httpd/wsgi')
        sudo('/etc/init.d/apache2 reload')


# INITIAL DATABASE CREATION

    prompt('Need human to setup django sqlite database user root passwd whatev. rtn=cont. Exit from shell to cont.')
    open_shell(command='cd /opt/graphite/webapp/graphite/ && sudo python manage.py syncdb')

    sudo('chown -R www-data:www-data /opt/graphite/storage/')
    sudo('/etc/init.d/apache2 restart')
    sudo('cp /opt/graphite/webapp/graphite/local_settings.py.example\
 /opt/graphite/webapp/graphite/local_settings.py')


# START CARBON

    with fabric.context_managers.cd('/opt/graphite/'):
        sudo('./bin/carbon-cache.py start')



def install_statsd(graphitehost, 
                   graphiteport=2003, 
                   statsdport=8125):
    '''
    Install statsd node.js server, handled by supervisord

    useage::
    
      fab -H cnx4 -f fab_sys_graphite.py install_statsd:graphitehost=cnx4
    
    '''
    sudo('rm -rf %s' % STATSD_HOME)
    sudo('apt-get update')
    sudo('apt-get install -y python-software-properties git-core nodejs')

    sudo('git clone https://github.com/etsy/statsd.git %s' % STATSD_HOME)
    with fabric.context_managers.cd(STATSD_HOME):
        sudo('''cat > dConfig.js <<EOF        
{
  graphitePort: %s
, graphiteHost: "%s"
, port: %s
}
EOF
''' % (graphiteport, graphitehost, statsdport) )    
    sudo('cd /home/deployagent/statsd && node stats.js dConfig.js &')



    
