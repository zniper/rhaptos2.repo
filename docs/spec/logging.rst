===================
Logging - proposals
===================

I intend to keep logging as simple and as comprehensive as possible

Principles:

1. Logging takes several different forms

   * metric gathering
   * audit logging
   * administrative / devops

2. Each form has different needs

Metric gathering
----------------

The graphite approach is sufficient here 
We are able to flexibly gather any event we choose to put in code.

Audit logging
-------------

THis is the "traditional" logging.
We shall have each application output via stdout / stderr and pipe into 
both local syslog and a centralised remote syslog running on the logging machine


Administrative work
-------------------

I anticipate putting in a centralised dashboard (prob using the below template)
that will allow watching logs, graphite updates and potentially nagios warnings.
COllating it all on one place seems a sensible move.


.. figure:: logadmin.png 
   :scale: 50 %

