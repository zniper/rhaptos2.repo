=============
configuration
=============

The problem
===========

I want to have one place and only one place to put things like the nginx root directory.
But there are several processes that need to know, fabfiles, Makefiles, the repo code itself, and these usually demand different configuration files in different formats.

So, I have one configuration file, that explodes into several different formats, and is *then* read by the different dependant processes


so the process is as follows


1. preprocess/mother_of_all_conf is where the canonical constants are kept.

2. This then writes out at least two other conf files - conf.mk and staging_conf.py
   It probably needs to also write out  conf.py...

3. we can then run the deploy rpocess, which will extract from git, and do a simple search./replace for tokens in the code.



Summary
-------

We want to extract from github to local working copy.
At this point, before deployment we need to know 
  
a) the context we shall be working in (ie is this a deploy to developer office, or production)

We run the *preprocess* service to correctly set up the different configuration files for that context

Then we need to run the *staging* process to get the in-code constants correctly fixed.

At that point we can run fab files to deliver the code to the correct locations.


1. download from github to workingcopy
2. clone from workingcopy into staging dir, make stagingdir the PYTHONPATH (virtualenv?)
3. preprocess on stagingdir
4. stage on stagingdir
5. run fabfiles / make

