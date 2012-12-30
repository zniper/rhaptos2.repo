#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


import uuid
import json
import os, sys

from rhaptos2.common import conf
from rhaptos2.common import log
from rhaptos2.common.err import Rhaptos2Error

from rhaptos2.repo import get_app, dolog
app = get_app()

def get_metadata(uuid):
    """Given a `uuid`, return the metadata information in a json format.

    Alert - this is stright copy from model - cannot import as model imports security...
    .. todo:: sort out circular imports and responsibilities.
    """
    filename = "{0}.metadata".format(uuid)
    repodir = app.config['repodir']
    file_path = os.path.join(repodir, filename)
    try:
        with open(file_path) as f:
            data = json.load(f)
    except IOError:
        data = {}
    return json.dumps(data)
#########################################


class WorkSpace(object):
    """Represents the set of NodeDocs the user can currently view

    I intend to use some backing file system, such as Riak (or just text)
    But for now this totally in efficient method will suffice.

    I will open each JSON doc in the repo, when a user makes workspace request
    and I will read them all and find which ones they are allowed to read /

    Arrggh


    TODO: test some means of writing files
    I want to write os.environ remote_e2repo, then write files to it.  Need
    some doctest fixtures ??

    >> u = WorkSpace('paul@mikadosoftware.com')
    >> u.files

    >> u.annotatedfiles


    """
    def __init__(self, user_id):
        """ """
        dolog("INFO", "in workspace of %s" % user_id,
              caller=WorkSpace, statsd=['rhaptos2.repo.workspace.entered',])

        self.user_id = user_id
        repodir = app.config['repodir']
        plain = []
        annotated = []
        files = [os.path.join(repodir, f)
                 for f in os.listdir(repodir)
                 # Check for the file extension.
                 if len(f.split('.')) < 2]

        for fpath in files:
            if not os.path.isdir(fpath):
                ndoc = NodeDoc()
                ndoc.load_from_file(fpath)
                if user_id in ndoc.contentrw:
                    plain.append(os.path.basename(fpath))
                    annotated.append({'id': os.path.basename(fpath),
                                     'title': ndoc.title
                                     })
        self.files_plain = plain
        self.files_annotated = annotated

    @property
    def files(self):
        return self.files_plain

    @property
    def annotatedfiles(self):
        return self.files_annotated



class NodeDoc(object):
    """Represents the node (section) stored on disk

    A NodeDoc is a JSON document, holding the following information

    v.0.1
    nodedocversion (0.1) - This will undergo a lot of changes.
    uuid : uuid representing this *section* - it is not a versioning tool.
           uuid is per document (ie a section or a chapter).  We can have many versions
           of the same uuid
    title: title of document (unicode)
    content: html5 payload.
    aclrw:     list of OpenID's that have the right to RW this list
    #acl-ro:     list of OpenID's that have the right to read acl-rw.  Defaults to acl-rw.
    contentrw: list of OpenID's that have the right to RW all items other than acl-rw / ro
    #content-ro: as above

    #POST (create new)
    #PUT (update the current uuid)
    #DELETE
    #GET



    """

    def __init__(self):
        self.nodedocversion = "0.1"
        self.versionkeys = ['aclrw', 'body', 'contentrw', 'uuid', 'title', 'language', 'subjects', 'keywords', 'authors', 'copyrightHolders']

    def load_from_file(self, uid):
        """find a file and load up the json doc and store internally

        We load a file if uid is anything other than blank
        Need lots of testing...
        NB - we MUST load the uid ON OUR DISK.  WE DO NOT TRUST acl settings SENT IN

        todo: split out parser and allow for versioning
        todo: make it vastly better

        Again tests need to be repeatable on Jenkins -
        sort out doctest fixtures

        >> c = NodeDoc()
        >> c.load_from_file('efe3e9bc-b345-4dec-b6dd-cd43e63e82ca')
        >> c.title
        u'There and back again'
        >> assert c.uuid == u'abcdefg'
        >> c.update('paul@mikadosoftware.com', title='foobar')
        F...
        >> c.update('paul@mikadosoftware.com', title='foobar2', content="little")
        F...

        ### But an openid user that is not in the list ...
        >> c.update('paul@noauth.com', title='foobar')
        Traceback (most recent call last):
           ...
        Rhaptos2Error: unauthorised
        >> c.save()
        S...
        >> c = NodeDoc()
        >> c.load_from_file('junk')
        >> assert c.uuid is None



        """
        #retrieve any metadata assoc with this,
        metad = json.loads(get_metadata(uid))

        repodir = app.config['repodir']
        filepath = os.path.join(repodir, uid)
        v01keys = self.versionkeys

        try:
            nodedict = json.loads(open(filepath).read())
        except:
            nodedict = dict(zip(v01keys, [None, None, None, None, None]))

        #if sorted(nodedict.keys()) != v01keys:
        #    raise  Rhaptos2Error("NodeDoc has incorrect keys - version 0.1" + str(nodedict.keys()) + str(v01keys))

        self.__dict__.update(nodedict)
        self.__dict__.update(metad)

    def load_from_djson(self, djson):
        """given a dict (from the JSON POST) create internal object

        Returns None, its updating internally.
        """



        v01keys = self.versionkeys
        #if sorted(djson.keys()) != v01keys:
        #    raise  Rhaptos2Error("Incoming JSON has incorrect keys" + \
        #              str(djson.keys()) + str(v01keys))
        if not djson['id'] : djson['id'] = str(uuid.uuid4())
        self.__dict__.update(djson)



    def update(self, user_id, **kwds):
        """update internal dict with whatever sent in kwds, plus some checking, """
        change_all = self.allow_other_change(user_id)
        change_acl = self.allow_acl_change(user_id)

        if change_all == False:
            raise Rhaptos2Error("unauthorised")

        for key in kwds:
            #if key in self.versionkeys:
                if key == 'aclrw' and change_acl == False:
                    raise Rhaptos2Error("Unauthorised")
                else:
                    self.__dict__[key] = kwds[key]

    def save(self):
        """ """
        if self.id == None:
            raise Rhaptos2Error("Need a ID to save")
        print "Saving"
        repodir = app.config['repodir']
        filepath = os.path.join(repodir, self.id)
        ###aaarrgh check keys
        d = {}
        for k in self.versionkeys:
            d[k] = self.__dict__[k]
        open(filepath, 'wb').write(json.dumps(d))


    def allow_acl_change(self, user_id):
        """ """

        if user_id in self.aclrw:
            dolog("INFO", "Found %s in %s" % (user_id, self.aclrw))
            return True
        else:
            dolog("INFO", "Not Found %s in %s" % (user_id, self.aclrw))
            return False

    def allow_other_change(self, user_id):
        """ """
        if user_id in self.contentrw:
            dolog("INFO", "Found %s in %s" % (user_id, self.contentrw))
            return True
        else:
            dolog("INFO", "Not Found %s in %s" % (user_id, self.contentrw))
            return False


if __name__ == '__main__':

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
