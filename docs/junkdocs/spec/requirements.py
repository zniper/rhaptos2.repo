#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


req = {
"Module Editor": [
['WYSIWYG HTML 5 Editor', 'Edit without viewing Source'],
['WYSIWYG HTML 5 Editor', 'Ability to insert processing instructions'],
['WYSIWYG HTML 5 Editor', 'Drag and Drop elements on a module'],
['WYSIWYG HTML 5 Editor', 'HTML pasted in should be restricted to the subset allowed'],
['WYSIWYG HTML 5 Editor', 'Drag and drop images into the editor'],
['WYSIWYG HTML 5 Editor', 'Split module into multiple modules'],
['PDF Preview', 'Calls out to PDF service'],
['Web View Preview', 'Calls out to Web View'],
['Web View Preview', 'Allow mobile and full web preview'],
['Edit roles', 'Links at top of module editor'],
['Edit Links', 'Links at top of module editor'],
['Edit Metadata', 'Links at top of module editor'],
['Edit Metadata', 'Subject is required'],
['Imports (Word, LaTeX, CNXML, HTML, Zip)', 'Imports performed by Transformation services'],
['Exports (HTML, ZIP, CNXML)', 'Uses Transformation services?'],
['Edit Files', 'Add, replace and delete images and other media files'],
['Publish', 'Pushes content to published repository'],
['Publish', 'Accept License and enter description'],
['Save', 'Saves to local repository'],
['Storage', 'Store unpublished modules and related files'],
['Storage', 'Should have API so any database can be used for storage'],
['Sword', ''],
['Derive a copy', ''],
['Math', ''],
['Small changes on published content', ''],
['Editor sandbox to allow users to try the editor without having an account', ''],
['Test publish option', ''],
['Restrictions', 'Prevent empty modules from being published']
],

"Workspace": [
['Workspace', 'List of items owned or shared by user'],
['Workspace', 'Tagging in Workspace with filtering'],
['Workspace', 'Share module with others for editing; Add user IDs and assign roles'],
['Workspace', 'Share tags with other users; similar to adding users to a workgroup'],
['Workspace', 'Separate publish roles (author, editor, etc. ) from editing roles'],
['Workspace', 'Each document needs to have a owner that sets the publish roles'],
['Workspace', 'The copyright holder must be the one to publish (accept CC License)'],
],

"Collection Editor": [
['Drag and Drop editor', 'Reuse current editor'],
['Add multiple modules at a time', 'Search by user, title or module id'],
['Add multiple subcollections at a time', 'Reuse current editor'],
['PDF Preview', 'Calls out to PDF service; Async response'],
['PDF Preview', 'Editor will send a hash of hashes so repeated requests can be filtered'],
['Web View Preview', 'Calls out to Web View'],
['Edit Metadata', 'Links at top of collection editor'],
['Edit Metadata', 'Subject is required'],
['Edit roles', ''],
['Publish', 'Pushes content to published repository'],
['Publish', 'Accept License and enter description'],
['Save', 'Saves to local repository in an HTML5 format'],
['Storage', 'Store unpublished collections and related files'],
['Sword', ''],
['Derive a copy', ''],
['Test publish option', ''],
['Restrictions', 'Prevent empty collections from being published'],
],

"Unpub Repo": [
['Store unpublished modules and related files', '-'],
['Store unpublished collections and related files', '-'],
['Public API for pull and push', '-'],
],

"Transformation Services": [
['Word Importer', 'Upgrade to LibreOffice'],
['Word Importer', 'All functionality in current version'],
['Open Office Importer', 'All functionality in current version'],
['LaTeX Importer', 'All functionality in current version'],
['Google Doc Importer', ''],
['HTML Importer', 'Import HTML 5 documents'],
['Module Zip importer', 'Support CNXML amd HTML5'],
['CNXML to HTML5', ''],
['HTML5 to CNXML', ''],
['PDF Generation', 'All functionality in current version'],
['PDF Generation', 'Should accept a hash which is used to compare requests for the same content to be generated.  If the hashes match, the new request is ignored.  If the hashes do not match, the current process is killed and a new process started.'],
['EPUB Generation', 'All functionality in current version'],
['Complete Zip Generation', 'Need to define what is in a complete zip'],
['Offline HTML Zip', ''],
['API', 'Needs design work'],
['SWORD', ''],
['Admin', 'Ability to turn services on and off'],
['Admin', 'Ability to check status of services'],
['Admin', 'Ability to read log files of services'],
['Admin', 'Ability to kill running processes'],
],

"Pub Repo": [
['Stores Content', 'module like (pages)'],
['Stores Content', 'collection like (lists)'],
['Stores Users', 'metadata for roles in content'],
['Stores Generated files', 'PDF, EPUB, ZIP'],
['Stores some record of license acceptance', ''],
['Accepts publish requests from Editors', 'How will editors be trusted?'],
['Accepts publish requests from Editors', 'How will users be authenticated?'],
['Can proxies be setup?', ''],
['Store who agreed to CC License', ''],
],

"Admin":[
['Read log files', 'Web View'],
['Read log files', 'Web View Repository'],
['Read transaction logs', 'Repository'],
],


"Web View":[
['Simplify design', 'Current portlets available via some linkage'],
['Decorate based on microdata', ''],
['Include CC microdata', ''],
['author email address should not be visible on any web page, except editing email address.', ''],
['Has own repository', 'Stores lenses, author profiles'],
['Needs to accept preview requests', ''],
['LWB', 'Display color and logo'],
], 

"Users":[
['Login using outside authetication', 'OAuth, Open ID, Twitter, Google'],
['Only store id and token, no passwords', ''],
['Storage', 'Where will users be stored?  '],
['', 'Can they be in more than 1 location? editor and repository?'],
['Store user metadata', 'modules, collections, email address, lenses'],
['Mapping of existing user ids to new user ids', ''],
['Org Accounts', 'Where will their additional privileges be stored?'],
['Users should be able to select if they can be emailed if they are an author', ''],
],

"Lenses":[
['Tags', ''],
['Comments', ''],
['URLs', ''],
['Types', 'Member, Affiliated, Endorsed'],
['Siyavula Lenses', 'Open tags'],
['Siyavula Lenses', 'Lenses Organizers'],
['Lens Permissions', 'Public, Private'],
['Logo', ''],
['LWB', 'property available'],
['LWB', 'Color picker'],
]

}




for component in req:
    cols = []
    print
    print component
    print "~" * len(component)
    print 
    for row in req[component]:
        numcols = len(row)
        
        for idx, col in enumerate(row):
            try:
                if cols[idx] < len(col): cols[idx] = len(col)
            except IndexError, e:
                cols.insert(idx, len(col))
    
    line = ''    

    for col in cols:
        line += "="*col + " " 
        
    print line
    print "primary".ljust(cols[0]) + " " + "Secondary".ljust(cols[1]) 
    print line
    for row in req[component]:
        s = ''
        for idx, col in enumerate(row):
            s += col.ljust(cols[idx]) + ' '
        print s
    print line
     



