#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


import json
import uuid
import md5

def u():
    return uuid.uuid1()

def hashcontent(content):
    m = md5.new(content)
    return m.hexdigest()


sect = {"id":  "org.cnx.sect:d3911c28-2a9e-4153-9546-f71d83e41126",                    
        "version":"ad0d6c247e0f1347364d890ec2e9fb53",
        "title": "Introduction",               
        "content": """<h1>In CONGRESS, July 4, 1776.<h1>
<p>The unanimous Declaration of the thirteen united States of America,</p>

<p>When in the Course of human events, it becomes necessary for one
people to dissolve the political bands which have connected them with
another, and to assume among the powers of the earth, the separate and
equal station to which the Laws of Nature and of Nature's God entitle
them, a decent respect to the opinions of mankind requires that they
should declare the causes which impel them to the separation.</p>
""",
        "roles":    
            {
            "Authors": 
                ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],   
            "Maintainers": 
                ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],
             "Copyright Holders": 
                ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383",],
             },


        "versioning": {
            "e5df9b39e5b428a84341c100bfe260df": {
                "roles":    
                    {
                    "Authors": 
                        ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],   
                    "Maintainers": 
                        ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     "Copyright Holders": 
                        ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     },
             },

            "ad0d6c247e0f1347364d890ec2e9fb53": {
                "roles":    
                    {
                    "Authors": 
                        ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],   
                    "Maintainers": 
                        ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     "Copyright Holders": 
                        ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     },
             },
               

         },

}





col  = {"id"      : "org.cnx.col:d3911c28-2a9e-4153-9546-f71d83e41126",
        "version": "238fhf8tr75hfjnhfuy9858",


        "metadata": {"Title": "United States Declaration Of Independance",
                     "Language": "English",
                     "subtype":  "Other Report",
                     "Subjects": ["Social Sciences",],
                     "Keywords": ["Life", "Liberty", "Happiness"],
                     "Summary": "No."
                    },

        "roles":    {"Authors": ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     "Maintainers": ["org.cnx.user:f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     "Copyright Holders": ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383",],
                     "aclrw": ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3\
383",],
                     "contentrw": ["org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3\
383",],
                    },

         

         "parameters": {"style": "LaTeX",
                        "font": "Times"
                       },

         "contents": [ ['org.cnx.sect.9d1d5c54-4066-410a-b9bc-9615ff3ff789',
                        ['org.cnx.sect.cc0a1460-11e8-4233-8e76-25b2d7020f8b',
                         'org.cnx.sect.90d7a34d-a5b3-4da1-8917-015cd67a3991'],
                       ],
                       ['org.cnx.sect.582d18be-dacf-45e4-af28-b79e7a465638',
                         ['org.cnx.sect.6d0b340f-de3f-413e-997e-dbff4eee29ad',
                          'org.cnx.sect.d3911c28-2a9e-4153-9546-f71d83e41126']
                       ],
                           'org.cnx.col.d3911c28-2a9e-4153-9546-f71d83e41126' 
                     ]
         
       }




user = {"id": "org.cnx.user:user.cnx.org.f9647df6-cc6e-4885-9b53-254aa55a3383",
        
        "details":{"FullName": "Thomas Jefferson",
                   "email":   "tom@Jefferson.com",
                   "Address" : "1 Arcacia Avenue, London",
                  },

        "openids": ["https://www.google.com/accounts/o8/id?id=AItOawlc7oYk8MNlwBgxCwMhLDqzXq1BXA4abbk", 
                    "http://openid.cnx.org/pbrian"
                   ],
        "version":  "1.0.0"
        }


print json.dumps(col, sort_keys=True, indent=4)
print json.dumps(sect, sort_keys=True, indent=4)
print hashcontent(sect["content"])
print json.dumps(user, sort_keys=True, indent=4)
