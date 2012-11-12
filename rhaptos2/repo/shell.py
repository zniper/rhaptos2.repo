#!/usr/bin/env python

import warnings
warnings.warn("This script to be rewritten in app facotry style")

import os
import readline
from pprint import pprint

from flask import *
from rhaptos2.repo import *

os.environ['PYTHONINSPECT'] = 'True'
