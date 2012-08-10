============
User details
============

JSON formatted document, holds all relevant details on a 
user.  Must conform to minimum amount of data, is versioned.

User ID
=======

We shall create a new, distributable and federatable user id of the
follwoing form::

   repo domain name reversed, with uuid in urn string format

   org.cnx.users.f81d4fae-7dec-11d0-a765-00a0c91e6bf6

   giving us a userid that is unique, linked to originating repo, so
   it can be traced back to a given source and fairly easily details
   requested from it.






::

    Python:

        user = {"id": "org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383",
        
        "details":{"FullName": "Paul Brian",
                   "email":   "paul@mikadosoftware.com",
                   "Address" : "1 Arcacia Avenue, London",
                  },

        "openids": ["https://www.google.com/accounts/o8/id?id=AItOawlc7oYk8MNlwBgxCwMhLDqzXq1BXA4abbk", 
                    "http://openid.cnx.org/pbrian"
                   ],
        "version": "1.0.0"
        }



       print json.dumps(user, sort_keys=True, indent=4)


AS JSON form:

::  

   JSON:

    {
	"details": {
	    "Address": "1 Arcacia Avenue, London", 
	    "FullName": "Paul Brian", 
	    "email": "paul@mikadosoftware.com"
	}, 
	"id": "org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383", 
	"openids": [
	    "https://www.google.com/accounts/o8/id?id=AItOawlc7oYk8MNlwBgxCwMhLDqzXq1BXA4abbk", 
	    "http://openid.cnx.org/pbrian"
	], 
	"version": "1.0.0"
    }
