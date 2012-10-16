# -*- coding: utf-8 -*-
"""test_app.py - ???

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from rhaptos2.repo import dolog, set_logger, set_app
from rhaptos2.repo.run import make_app

def test_can_log():
    app = make_app()

    dolog('WARN', 'Help')
    # ??? How do we know this worked? The nature of logging in python
    #     is to log even if a handler hasn't been registered. We
    #     should have a handler set up here to catch log messages.
