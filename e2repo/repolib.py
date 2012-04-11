#!/usr/local/bin/python
#! -*- coding: utf-8 -*-

'''
:author: pbrian <paul@mikadosoftware.com>

the repository manager for editorv2 (e2) is designed to simply service 
GET POST PUT and DELETE requests for modules, collections [and lenses]

The initial stub version will simply support writing to a single directory as text files.


'''

import os


MAINDIR = '/tmp/e2repo'
MODULEDIR = os.path.join(MAINDIR, 'modules')
COLLECTIONDIR = os.path.join(MAINDIR, 'collections')
LENSDIR = os.path.join(MAINDIR, 'lenses')

def getfilepath(text, name, cnxtype):
    '''given details of the module, return the filepath to write to '''
    return os.path.join(MODULEDIR, 'foo.txt')

def POST(text, name, cnxtype):
    '''
    cnxtype one of LENS MODULE COLLECTION
     
    '''
    f = getfilepath(text, name, cnxtype)
    open(f, 'w').write(text)
    return f  
    

def DELETE(text, name, cnxtype):
    pass

def PUT(text, name, cnxtype):
    pass

def GET(text, name, cnxtype):
    pass
