
=========
memcached
=========



We are not attempoting to runa cluster for now, or invalidate entries - this is solely a placeholder for a lookup on userid/openid

::

  sudo apt-get install memcache

edit /etc/memcached.conf

  -l 127.0.0.1
  This is about all the security memcache has - so for now its just localhost only

  bit less memory consumption is also useful
  -m 16
  caps at 16 MB not 64 the default.  For dev this is fine.

Telnet testing
--------------


set requires::  

   set <key> <flags> <exptimeinSecs> <bytes> /r/n<Value>/r/n

   so set key "foo" to "test" for 5 mins, no flags

   set foo 0 300 4
   test

   STORED



get <key>

Return all keys in memcache

(see this site, bit awkward)

::

    deployagent@devweb:/tmp/repo$ telnet localhost 11211
    Trying 127.0.0.1...
    Connected to localhost.
    Escape character is '^]'.
    set foo 0 300 4
    test
    STORED
    get foo
    VALUE foo 0 4
    test
    END




Python usage
------------
::

    import memcache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    mc.set("some_key", "Some value")
    value = mc.get("some_key")
