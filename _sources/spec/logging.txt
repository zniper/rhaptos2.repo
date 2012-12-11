===================
Logging - proposals
===================

I intend to keep logging as simple and as comprehensive as possible

Principles:

1. Log through stdout
2. add as much checking as possible to make auditing simpler
3. write tools and centralise stuff (dashboard) to encourage reuse of tools
4. use metrics as a guide.

Example use
-----------

We have a rhaptos2.common project which contains the generic logging code.
This means all projects (even if they want projects not to do with CNX)
can use the same API to log their events, and do so in a consistent manner

The code is set up to use a custom python logger, and a statsd-client
to send audit logs to a centralised sysloging server, and a metric gathering 
graphite server

Example call::

    app.logger.info(
               msg="PUT of module abcd-1234-4443-44 by userid xxx"
               events=["rhaptos2.repo.module.put", "cnx.users.xxx"]
               ) 


context
-------

Whilst a log message can contain whatever the developer needs to say,
we can expect to always get the below data passed in - making filtering 
the output much easier.

userid - the cnx based id of a user, that is mapped to a "real" openid / address by rhaptos2.user

component - there is no hard and fast definition of a component, but its best thought 
            of as a discrete unit, doing some useful work for us.

event tags - these are defined as strings - they are quite arbitrary but it is useful for us 
             to keep a simple hierarchy - like rhaptos2.repo.module / collection

time & server & running instance



Output filtering
----------------

We will get a *lot* of logs.  At the moment we capture x MB / mth
We could expect to conservatively increase that by 50% simply by gathering in 
more detail.

Filtering the output is at the moment a simple affair (grep).
We shall develop tools to filter the output in more consistent means 


Metric gathering
----------------

The graphite approach is sufficient here 
We are able to flexibly gather any event we choose to put in code.

We should be able to watch our metrics overtime as follows

.. figure:: ../graphite_load_bal.png
   :scale: 50 %

At the moment graphite has been left alone - we really need to put some load tests up 
and see what we collect / performance issues.
Other than that the systems work well and as expected.


Audit logging
-------------

This is the "traditional" logging.
We shall have each application output via stdout / stderr and pipe into 
both local syslog and a centralised remote syslog running on the logging machine


This is the simplest approach we can devise - rsyslog is old reliable technology
I do not want to use print stmts, but create a log class that can take "extras" (yes its called that)
and we just log with say the requestid in it.


Administrative work
-------------------

I anticipate putting in a centralised dashboard (prob using the below template)
that will allow watching logs, graphite updates and potentially nagios warnings.
COllating it all on one place seems a sensible move.


.. figure:: logadmin.png 
   :scale: 50 %

This is mostly a centralising approach - nice to have, and will help.  Just not
viital
