#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###

from werkzeug.exceptions import HTTPException

class Rhaptos2Error(Exception):
    pass


class Rhaptos2SecurityError(Exception):
    pass

class Rhaptos2AccessNotAllowedError(HTTPException):
    code = 403
    description = "Attempt to access a component you do not have access to"
    
