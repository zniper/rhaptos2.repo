#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


Staff = [("Paul Brian", "paul@mikadosoftware.com"),
          ("Ed Woodward", "ecw1@rice.edu"),
          ("Jessica Burnett", "jess@cnx.org"),
          ("Philip Schatz", "phil@cnx.org"),
          ("Ross Reedstrom", "reedstrm@rice.edu"),
          ("Marvin Reimer", "therealmarv@gmail.com"),
          ("Michael Mulich", "michael@mulich.com"),
]

gsoc = [          
          ("Saket Choudray", "-"),
          ("Debajyoti Datta", "-"),
          ("Alasdair Corbett", "-"),
          ("Yanchai Ye", "-"),         
]

emails = gsoc

import md5

gravatar_urls = {}


for name, email in emails:
    email = email.strip().lower()
    m = md5.new(email)
    h = m.hexdigest()
    gravatar_urls[name] = "http://www.gravatar.com/avatar/%s" % h


x = []
for name in gravatar_urls:
    x.append( """<td>%s</td><td><img src="%s" /></td>""" % (name, gravatar_urls[name]))

print "<table><tr>"
for i, val in enumerate(x, start=1):
    print val
    if i % 3 == 0: print "</tr><tr>"
print "</table>"

    
