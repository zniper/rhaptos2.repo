#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


from rhaptos2.repo import app
d = {
     'rhaptos2_use_logging':'Y',
     'rhaptos2_loglevel':'DEBUG',
      'rhaptos2_repodir':'/tmp/repo',
      'rhaptos2_statsd_host':'log.frozone.mikadosoftware.com',
      'rhaptos2_statsd_port':'8125',
      'rhaptos2_www_server_name':'www.frozone.mikadosoftware.com',
      'rhaptos2_cdn_server_name':'www.frozone.mikadosoftware.com',
      'BUILD_TAG':'WHATDOWEDOHERE'}
app.config.update(d)
app.config["TESTING"] = True
tclient = app.test_client()
rv = tclient.get('/')
rv = tclient.get('/version/')
assert "0.0.4" in rv.data
print rv.data


