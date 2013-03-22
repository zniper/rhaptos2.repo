

* create _authenticatedIdentiferRecvd_ method, both persona openid can call it
 
* create a test pkg for use by bamboo as testing

* get the docs working

* cleaner bamboo run

* get nosetests to have fixtures

* integrate JS

* rename frozone to author_tools.js and split up if needed

* discuss with phil / pumazi best JS script approach

* user: define single user detail

* user: Existing user return details matching one identifer

* user: No user details stored, return 404 on GET,
       
* User: no user detials - POST - MUST supply identifer
        supply uuid
        Some form of JS that reads a mediatype (json) and captures ...?
 
* user: write the user spec

* user: stubout 

* repo: get US consittuion working

* repo: 

============
Repo Roadmap
============

This is a roadmap of desired milestones - they are exepcted to be the x in versioning 1.x.0


* Integrate oerpub/whysiwhat editor into the CI build
* ensure CI build builds completely, and runs maaster builds for every component
* get single US declaration of independance as a test / testable document 
* Handle all JSON conversion and CORS by convention  
  pass a dict througout and only convert to response object at view.
  Is this most sensiuble means?
* Place system wide integration tests into commonly available calls so 
  can visit each repo and run all tests
* Protocol beteen editor and Authoring tools
  - images / resources
  - html5
  - save, load, delete, update, 
  - workspace handling
* simple shared message bus - probably overkill
* Editor Client API
  - load_document
  - load_list_of_documents
  - save_new_document
  - save_list_of_resources
  - save_resource




Blue Sky
--------

* Split common REST based handling for flask into a lib
* Riak as backend jSON store


Communication between editor and author tools client 
====================================================

This is all on browser javascript, and in the same process / namespace.
So there *may* be some technical messaging issues, but mostly we shall try to support 
a simple API

We will not try and use a message bus.

All API calls will be lexically namespaced JS function calls.
The AuthorTools will supply author_ apis, the editor will supply ed_
Each module will supply its won calls, we shall need to test for 
existennce of calls

We shall version each API call.  All initial versions will be "0.5"
This string will be passed as first argument to all api calls

   save_image("0.5", DOM-REF)

The suggested calls
-------------------

Editor
------

* ed_load_html(ver, documentRef, str)
  Place in the DOM at DOM ref documentref, the string str 
  which will be a valid HTML5 document

* ed_get_all_components(ver, documentRef)
  
  

Author tools
------------

* author_save_html

