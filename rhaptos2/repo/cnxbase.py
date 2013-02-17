
"""
THis exists solely to provide less typing for a "leaf node"
in a simple realtional schema (1:M and 1:M-N:1) when used with SQLAlchemy

SA does not support class based inheritence in the normal Python way for objects inheriting from Base.  Thus we have those objects perform multiple inheritence...


"""
import json
import sqlalchemy.types
import datetime


class CNXBase():

    def from_dict(self, userprofile_dict):
        """
        SHould test for schema validity etc.

        """
        d = userprofile_dict
        for k in d:
            setattr(self, k, d[k])

    def to_dict(self):
        """Return self as a dict, suitable for jsonifying """

        d = {}
        for col in self.__table__.columns:
            d[col.name] = self.safe_type_out(col)
        return d

    def jsonify(self):
        """Helper function that returns simple json repr """
        selfd = self.to_dict()
        jsonstr = json.dumps(selfd)  # here use the Json ENcoder???
        return jsonstr


    def safe_type_out(self, col):
        """return the value of a coulmn field safely for json
        This is essentially a JSONEncoder sublclass inside object - ...
        """
        ##XXX cannot get isinstance match on sqlalchem types
        if str(col.type) == "DATETIME":
            try:
                outstr = getattr(self, col.name).isoformat()
            except:
                outstr = None
        else:
            outstr = getattr(self, col.name)
        return outstr


    # def safe_type_out(self, col):
    #     """return the value of a coulmn field safely as something that
    #        json can use This is essentially a JSONEncoder sublclass
    #        inside this object.
    #     """
    #     print col.type, type(col.type)
    #     if (isinstance(type(col.type), sqlalchemy.types.DateTime) or
    #         isinstance(type(col.type), datetime.datetime)):
    #         outstr = str(getattr(self, col.name).isoformat())
    #     else:
    #         outstr = getattr(self, col.name)
    #     return outstr



    def set_acls(self, setter_user_uuid, acllist, userrole_klass=None):
        """set the user acls on this object.

        inheriting from CNXBase implies we are modelling
        a resource, and we want to control Read?write of the resource
        through ACLs - which are represented in dbase as userrole_<resource>

        NB whilst practical to use one userrole table and preferable
        SQLAlchemy seems to place limits on it. and I dont want to
        muck about.

        SOme, not all objects that inherit form CNXBase (!)
        will have a relatred user_roles table.
        This will map the object ID to a acl type and a user


        [{'date_lastmodified_utc': None,
          'date_created_utc': None,
          'user_uuid': u'Testuser1',
          'role_type': 'author'},
         {'date_lastmodified_utc': None,
          'date_created_utc': None,
          'user_uuid': u'testuser2',
          'role_type': 'author'}]



        """
        ##is this authorised? - sep function?
        if (setter_user_uuid, "aclrw") not in [(u.user_uuid, u.role_type)
                                               for u in self.userroles]:
            raise Rhaptos2Error("http:401")
        else:
            for usrdict in acllist:
                #I am losing modified info...
                self.adduserrole(userrole_klass, usrdict)

    def adduserrole(self, userrole_klass, usrdict):
        """ keeping a common funciton in one place

        Given a usr_uuid and a role_type, update a UserRole object

        I am checking setter_user is authorised in calling function.
        Ideally check here too.
        """
        t = self.get_utcnow()

        ##why not pass around USerROle objects??
        user_uuid = usrdict['user_uuid']
        role_type = usrdict['role_type']

        if user_uuid not in [u.user_uuid for u in self.userroles]:
            # UserID is not in any assoc. role - add a new one
            i = userrole_klass()
            i.from_dict(usrdict)
            i.date_created_utc = t
            i.date_lastmodified_utc = t
            self.userroles.append(i)

        elif (user_uuid, role_type) not in [(u.user_uuid, u.role_type) for u
                                             in self.userroles]:
            # UserID has got a role, so *update*
            i = userrole_klass()
            i.from_dict(usrdict)
            i.date_lastmodified_utc = t
            self.userroles.append(i)
        else:
            #user is there, user and role type is there, this is duplicate
            pass

    def get_utcnow(self):
        """Eventually we shall handle TZones here too"""
        return datetime.datetime.utcnow()
