

####### logging config
import logging
SYSLOG_SOCK='/dev/log'
LOGLEVEL=logging.DEBUG

######### server disk paths

remote_e2repo = '/usr/share/www/flask/e2repo'

TINYMCE_STORE = '/tmp/tinymce'
remote_wwwd = '/usr/share/www/nginx/www'
remote_supervisor_home = '/home/deployagent/supervisor'

remote_git_repo = 'git://github.com/lifeisstillgood/frozone.git'
remote_e2server = '/usr/share/www/flask/e2server'
remotehomedir = '/home/deployagent'
remote_sitepackage = '/usr/local/lib/python2.7/dist-packages'

localstagingdir = '/tmp/mikado/staging'
localgitrepo = '/tmp/mikado/git'



context = {
 '<<CDN-SERVER-NAME>>': 'cdn.office.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',


 '<<E2SERVERROOT>>': remote_e2server,
 '<<E2REPOROOT>>': remote_e2repo,


 '<<DNSFORWARDERS>>':  '208.67.222.222',
 '<<ZONENAME>>': 'office.mikadosoftware.com',
 '<<ZONEFILENAME>>': 'com.mikadosoftware.office.db',
 '<<REVZONENAME>>': '0.0.10.in-addr.arpa',
 '<<REVZONEFILENAME>>': 'rev.0.0.10.in-addr.arpa',

                     }




