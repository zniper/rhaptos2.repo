======================================
A clever solution to the wrong problem
======================================

I have completed a clever solution to a problem.  Unfortunately, its
probably the wrong problem.


The problem was fairly simple.  I had built a simple web services
demonstration, and then surrounded it with supporting services, like
logging, continuous builds, statsd/graphite servers.  All good,
eco-system like stuff.

And hosted on virtual servers on a private IP address space.

So, you had to be on my LAN in my office to view it. Since I was
working remotely, and was the only person actually in my office, this
was a bit of a problem.  In fact this is the *real* problem.

I could get you to tunnel in, VPN in, and see it but it seemed better
if I rebuilt the system over in your neck of the woods.  So initially
I set up the service on frozone.office.mikadosoftware.com, a rackspace
hosted server.  That worked, but there was only a web server and a
repository, no CI, no logging server, no messaging server.


So, I decided to recreate my LAN in your LAN, that way we can use one
location as the 'most recent build' or the 'beta' service.  But we
only had one physical host, and with only one routable IP [#]_

And, well, with some help, it worked.  I can now build a virtual,
NAT'd LAN inside a Linux host, which is pretty cool and has some
interesting, useful and cost-saving applications.

Its just that its still not on your LAN.  Its on another (virtual)
NAT'd LAN just like my office.  It took me a while to notice.  I was
wondering what that vague nagging feeling had been.

So, a comment Kathi made come back to me - they buy racksp[ace virtual
instances when they need a new server.

Well why don't I just expand the one server I was using as a demo, but
three or more as I need.

And I did that.  And got oddly scared.  Not scared so much, more,
well, here are 3 hosts on the public internet, I am about to make one
a logging server, one a jenkins server.  How do I lock those down on
the *public* internet?

And then ...

This really will be developing in the open.

Release the code, test it in the open, build it on public servers.

I am a big advocate of DevOps - building the operational systems and
support at the same time as the 'real' code, so that the solutions to
managing a system are baked-in deeply and naturally, not tacked on at
the last minute by harrased sysadmins.


Now, even so the final release to live is usually a big deal, security
issues come to the front, lots of performance testing, SecPen,
reworking and rethinking.

But what if all of that had already been done - built alongside the
apps themselves.

This asumptions that each server is on its own in a hostile
environment, is attractive to the idea we design complex systems in a
eco-system, and that they should be capable of surviving without the
DMZ.






.. [#]  technically two NIC cards and a backplane and ... but effectively just one server one IP.
