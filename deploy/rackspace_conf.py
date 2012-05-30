#!/usr/local/bin/python

'''
supply farily manipulakle config
'''


####### logging config
import logging
SYSLOG_SOCK='/dev/log'
LOGLEVEL=logging.DEBUG

######### server disk paths



TINYMCE_STORE = '/tmp/tinymce'
remote_wwwd = '/usr/share/www/nginx/www'
remote_supervisor_home = '/home/deployagent/supervisor'

remote_sitepackage = '/usr/local/lib/python2.7/dist-packages'

remote_git_repo = 'git://github.com/lifeisstillgood/frozone.git'
remote_e2repo = '/usr/share/www/flask/e2repo'
remote_e2server = '/usr/share/www/flask/e2server'
remotehomedir = '/home/deployagent'

localgitrepo = '/tmp/mikado/git'
localstagingdir = '/tmp/mikado/staging'

statsd_host = 'log.frozone.mikadosoftware.com'
statsd_port = 8125

#######################

context = {
 '<<CDN-SERVER-NAME>>': 'cdn.frozone.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'www.frozone.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.frozone.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',

 '<<LOGSERVERFQDN>>': 'log.frozone.mikadosoftware.com',
 '<<LOGSERVERPORT>>': '5514',
 

 '<<E2SERVERROOT>>': remote_e2server,
 '<<E2REPOROOT>>': remote_e2repo,
 '<<WSGIPORT_E2SERVER>>': '127.0.0.1:8001',
 '<<WSGIPORT_E2REPO>>': '127.0.0.1:8002',


 '<<DNSFORWARDERS>>':  '208.67.222.222',
 '<<ZONENAME>>': 'office.mikadosoftware.com',
 '<<ZONEFILENAME>>': 'com.mikadosoftware.office.db',
 '<<REVZONENAME>>': '0.0.10.in-addr.arpa',
 '<<REVZONEFILENAME>>': 'rev.0.0.10.in-addr.arpa',

                     }
