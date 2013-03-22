==========
Collection
==========

As JSON

:: 

    {
	"contents": [
	    [
		"9d1d5c54-4066-410a-b9bc-9615ff3ff789", 
		[
		    "cc0a1460-11e8-4233-8e76-25b2d7020f8b", 
		    "90d7a34d-a5b3-4da1-8917-015cd67a3991"
		]
	    ], 
	    [
		"582d18be-dacf-45e4-af28-b79e7a465638", 
		[
		    "6d0b340f-de3f-413e-997e-dbff4eee29ad", 
		    "d3911c28-2a9e-4153-9546-f71d83e41126"
		]
	    ]
	], 
	"metadata": {
	    "Keywords": [
		"Life", 
		"Liberty", 
		"Happiness"
	    ], 
	    "Language": "English", 
	    "Subjects": [
		"Social Sciences"
	    ], 
	    "Summary": "No.", 
	    "Title": "United States Declaration Of Independance", 
	    "subtype": "Other Report"
	}, 
	"parameters": {
	    "font": "Times", 
	    "style": "LaTeX"
	}, 
	"roles": {
	    "Authors": [
		"org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
	    ], 
	    "Copyright Holders": [
		"org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
	    ], 
	    "Maintainers": [
		"org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
	    ], 
	    "aclrw": [
		"org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
	    ], 
	    "contentrw": [
		"org.cnx.user.f9647df6-cc6e-4885-9b53-254aa55a3383"
	    ]
	}
    }


As Python

::

    col  = {"metadata": {"Title": "United States Declaration Of Independance",
			 "Language": "English",
			 "subtype":  "Other Report",
			 "Subjects": ["Social Sciences",],
			 "Keywords": ["Life", "Liberty", "Happiness"],
			 "Summary": "No."
			},
	    "roles":    {"Authors": ["org.cnx.user:user.cnx.org-f9647df6-cc6e-4885-9b53-254aa55a3383",],
			 "Maintainers": ["org.cnx.user:user.cnx.org-f9647df6-cc6e-4885-9b53-254aa55a3383",],
			 "Copyright Holders": ["org.cnx.user:user.cnx.org-f9647df6-cc6e-4885-9b53-254aa55a3383",],
			 "aclrw": ["org.cnx.user:user.cnx.org-f9647df6-cc6e-4885-9b53-254aa55a3383",],

			 "contentrw": ["org.cnx.user:user.cnx.org-f9647df6-cc6e-4885-9b53-254aa55a3383",],
			},

	     "parameters": {"style": "LaTeX",
			    "font": "Times"
			   },

	     "contents": [ ['org.cnx.sect:9d1d5c54-4066-410a-b9bc-9615ff3ff789',
			    ['org.cnx.sect:cc0a1460-11e8-4233-8e76-25b2d7020f8b',
			     'org.cnx.sect:90d7a34d-a5b3-4da1-8917-015cd67a3991'],
			   ],
			   ['org.cnx.sect:582d18be-dacf-45e4-af28-b79e7a465638',
			     ['org.cnx.sect:6d0b340f-de3f-413e-997e-dbff4eee29ad',
			      'org.cnx.sect:d3911c28-2a9e-4153-9546-f71d83e41126']
			   ],
                           'org.cnx.col:d3911c28-2a9e-4153-9546-f71d83e41126' 
			 ]

	   }







Defintions
==========

contents 
--------

This is a single ordered list, containing zero or more other lists,
each list containing zero or more urns for either :doc:`section-doc`s,
:doc:`collection-doc`s (where a collection is itself going to contain
more sections etc etc.

The parsing of these into and out of (JSON) format and the assembly
and disassemlby of the html into docs will be a main focus of the
development work - although it should be realitviely simple, we shall
expect ot do it twice - Javascript and Python.


URN defintions
~~~~~~~~~~~~~~

We are simply namespacing and ignoring the traditional urn in front.


:dicuss: Federation - we are implicitly federating users - that is a userID is transferrable between repos because of the internal user.cnx.org-xxx.  Implying that user.cnx.org will always hold the canonical representation of :doc:`user-detail` and can be queried for latest.  So should we have same federation for sections?  It seems unlikely.  But somehow we must guarentee a connect between a urn and a live url.






metadata
--------


parameters

roles
-----

* Authors
