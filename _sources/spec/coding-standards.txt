==============
code standards
==============

We stick to PEP-8 in all cases except where we really need to not do so.  PEP-8 is basically our default.  Pylint should be run over checkins (Jenkins is / will be set up to do so)



json

When writing JSON to disk you MUST use sorted keys and fixed indentation so use:

   json.dumps(obj, sort_keys=True, indent=4)

This ensures that disk bound objects are always human readable, and directly comparable for testing purposes.

UUID

You MUST ask for UUID.uuid4() - it is not the traditional random plus time plus MAC address but relies on a /dev/random or /dev/urandom.  Frankly in modern ubuntu OS or FreeBSD that will have enough entropy that failure through collisions will occur long after every other bug we write takes out the site, and the asteroid gets us.

http://stackoverflow.com/questions/703035/when-are-you-truly-forced-to-use-uuid-as-part-of-the-design/786541#786541
