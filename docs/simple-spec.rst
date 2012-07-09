===========
Simple Spec
===========

Components 
==========

* Authoring Client

* unpub-repo

* pub-repo

* transform service

* print-queue

* logging & metrics

* authentication / authorisation


One paragraph descriptions
==========================


Authoring Client
----------------

A Javascript-based set of authoring tools, run on the client browser.  They allow

* editing of content of modules (WYSIWIG / WYSIWYM)
* editing of meta data around modules (see metadata)
* interaction with REST-services, knowledge of the server protocols
* cleaner interaction with browser and updates, potentially using client side templating

unpub-repo
----------

A Python based web service, adhereing closely to REST principles, that stores the current 
editing module, on the server, and provides resilience and robustness.

* Single sign on using OpenID technologies.
* robust, scalable backend storage and front end load balancing / applications


Files and images
----------------

* Capture URL of imported images, and as needed cpature, store as related file, ensure it has appropriate 
  licnsing

* 

dependancy chain of modules
---------------------------

navigation via collection
navigation via href
naviagation via bibliopgraphy
naviatiopons via link-ography
navigation via algo-suggestion



pub-repo
--------


transform service
-----------------


print-queue
-----------


logging & metrics
-----------------


authentication / authorisation
------------------------------


Security - is based on the security settings of the parent module.
Is based on author and mainters are allowed to use it.
What is a persons open id?



Meta Data
=========

Collection meta data
--------------------

JSON defintions....

'coltitle', String(128), 'Title of collection'
'collang', String(12), 'primary language for the collection'
'colsubtype', String(12), 'subtype, limited list incl course manual'
'colsubjectlist', 'Text'
'colkeywordslist', 'Text'
summary TEXT


Module Meta data
----------------

Do this in micro-formats

mdml-version
parent-uuid
repoistory-base-uri
this-uuid
mdtitle
mdversion
parent-created-date
this-created-date
actors-person-adr

MDML ::


    <metadata mdml-version="0.5">
      <md:repository>http://cnx.org/content</md:repository>
      <md:content-id>new</md:content-id>
      <md:title>ssh usage</md:title>
      <md:version>**new**</md:version>
      <md:created>2012/04/02 09:37:58.075 GMT-5</md:created>
      <md:revised>2012/04/02 09:37:58.546 GMT-5</md:revised>
      <md:actors>
	<md:person userid="pbrian">
	  <md:firstname>Paul</md:firstname>
	  <md:surname>Brian</md:surname>
	  <md:fullname>Paul Brian</md:fullname>
	  <md:email>paul@mikadosoftware.com</md:email>
	</md:person>
      </md:actors>
      <md:roles>
	<md:role type="author">pbrian</md:role>
	<md:role type="maintainer">pbrian</md:role>
	<md:role type="licensor">pbrian</md:role>
      </md:roles>
      <md:license url="http://creativecommons.org/licenses/by/3.0/"/>
      <!-- For information on license requirements for use or modification, see license url in the
	   above <md:license> element.
	   For information on formatting required attribution, see the URL:
	     CONTENT_URL/content_info#cnx_cite_header
	   where CONTENT_URL is the value provided above in the <md:content-url> element.
      -->
      <md:keywordlist>
	<md:keyword>ssh</md:keyword>
      </md:keywordlist>
      <md:subjectlist>
	<md:subject>Science and Technology</md:subject>
      </md:subjectlist>
      <md:abstract>Review of SSH</md:abstract>
      <md:language>en</md:language>
      <!-- WARNING! The 'metadata' section is read only. Do not edit above.
	   Changes to the metadata section in the source will not be saved. -->
    </metadata>
