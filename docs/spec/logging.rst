===================
Logging - proposals
===================

I intend to keep logging as simple and as comprehensive as possible

Principles:

1. Log through stdout
2. add as much checking as possible to make auditing simpler
3. write tools and centralise stuff (dashboard) to encourage reuse of tools
4. use metrics as a guide.


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
