

context = {
 '<<CDN-SERVER-NAME>>': 'cdn.office.mikadosoftware.com',
 '<<CDN-SERVER-ROOT>>': '/usr/share/www/nginx/cdn',
 '<<REPO-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-NAME>>': 'www.office.mikadosoftware.com',
 '<<WWW-SERVER-ROOT>>': '/usr/share/www/nginx/www',

 '<<DNSFORWARDERS>>':  '208.67.222.222',
 '<<ZONENAME>>': 'office.mikadosoftware.com',
 '<<ZONEFILENAME>>': 'com.mikadosoftware.office.db',
 '<<REVZONENAME>>': '0.0.10.in-addr.arpa',
 '<<REVZONEFILENAME>>': 'rev.0.0.10.in-addr.arpa',

                     }


####### logging config
import logging
SYSLOG_SOCK='/dev/log'
LOGLEVEL=logging.DEBUG

######### server disk paths

remote_e2repo = '/usr/share/www/flask/e2repo'
localstagingdir = '/tmp/mikado/staging'
TINYMCE_STORE = '/usr/home/pbrian/frozone/thirdparty/tinymce'
remote_wwwd = '/usr/share/www/nginx/www'
remote_supervisor = '/home/deployagent/supervisor'
localgitrepo = '/tmp/mikado/git'
localhomedir = '/tmp/mikado'
remote_git_repo = 'git://github.com/lifeisstillgood/frozone.git'
remote_e2server = '/usr/share/www/flask/e2server'
remotehomedir = '/home/deployagent'
