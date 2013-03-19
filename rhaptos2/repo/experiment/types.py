#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


import sqlalchemy.types as types

class SqlLiteArray(types.TypeDecorator):
    '''Allows SQLLite to use POSTGRES ARRAY type
    converts python list to and from comma deliminated string
    '''

    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        return ",".join(value)

    def process_result_value(self, value, dialect):
        return value.split(",")



#http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#typedecorator-recipes

