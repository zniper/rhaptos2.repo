

#uwsgi -s 127.0.1:8001 --module e2server --callable app --logto /tmp/e2server.log

uwsgi -s 127.0.1:8001 --module e2server --callable app 

