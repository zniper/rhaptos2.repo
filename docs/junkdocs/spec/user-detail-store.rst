==================
User Details Store
==================

The store for user details

This is expected to be in two parts for the initial 
1.0 milestone.  Each web app will have a localhost 
memcache instance, which will store the known users.

A second REST-based web app will be run on ONE server,
will be text file backed and will simply receive a formatted JSON document, and store it.

This server will also be able to pre-populate any given memcache instance, and will be able to cache-update if any user details change.

We are not currently looking at the security implications

