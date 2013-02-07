===========
Collections
===========


I am trying to see the bare minimum example 

Fred writes a book, called "What I did last summer"
He writes it using notepad on his local harddisk.


chapter1.html::

    <html>
    <body>
    I went to the Beach, and made a sandcastle.
    <a href="chapter2.html">next</a>
    </body>
    </html>    


chapter2.html::

    <html>
    <body>
    I had an ice cream.
    </body>
    </html>    



He decides to save and publish it on CNX.org
He uses the entirely javascript based, cnx-authoir-tools-suite.
This is loaded when he clicks on "publish" on cnx.org

He is prompted to "Create a book/report" - he names it "SummerHols".::

   POST collections/
   ...
   {name: "SummerHols"}

The repo.cnx.org returns::

   {"id": "org.cnx.col:27af5385-50db-41b8-b0c1-ba4a62e93c26",
    "name": "SummerHols"
    "contents": "[]"
   }

The JS client now shows Fred an empty tree under his "summerHols" and
a list of all his open tabs.  He drags and drops the tab icon called
chapter1 onto his book, and a tree display is updated: ::

 SummerHols/
    chapter1.html

He clicks "Save Book".  

1. The jsclient computes the md5 hash of chapter1.html *content*
2. The jsclient POSTS a JSON doc containing the content and metadata

::

  POST modules/
  ..
  {id:"org.cnx.module:80ff404cfa990b0c57afefc8ef955872",
   name:"chapter1.html"
   "content": "<html>...sandcastle...</html>"
  }

If the computed md5 matches the server calculated we accpet and return 200.
We store the json.

repo.cnx.org returns:

  200
  {id:"org.cnx.module:80ff404cfa990b0c57afefc8ef955872"}

3. The JSclient now updates the collection document.


  PUT collections/org.cnx.col:27af5385-50db-41b8-b0c1-ba4a62e93c26
 
   {"id": "org.cnx.col:27af5385-50db-41b8-b0c1-ba4a62e93c26",
    "name": "SummerHols"
    "contents": "[
                  [chapter1.html, "org.cnx.module:80ff404cfa990b0c57afefc8ef955872"],
                 ]"                                                                   
   }  




What is important in this discussion?
=====================================

We are not focusing on *modules* but on *collections*.
THis is because identity of modules is an uncertain, slippery thing.
We really have no effective way of tracking a module as it is edited, updated
or deleted outside of our (editor/repo) control.

We cannot really tell what is the "latest" version of a module.
THe desire to do so is understandable, but it leads to "deriving" works,
problems in merging, in brnaching etc.  

Simply put the "latest" version of a module is not a sensible question.

What is a sensible question is what is the latest Table of contents for a book,
in which our module used to be?

In short - Modules Must have context to make sense.  The context of a module is
a collection.  (it might be a workspace as well but work with me here)

We can give it a UUID, or a unique number or what have you.  But modules "meaning" 
does not stay the same through time.  It might be my chapter on Nero, your chapter on 
Rome, and someone else will edit it tomorrow to talk about flower arranging.

But in each case, that module sits in a table of contents for me, for you and for
the florist.  And the ToC points to different versions of the same module in time.

So it really does not make sense to talk of one unique module travelling through time.

So instead of latest version of module 3456, we should ask for the latest version
of the module that is 1st in the collection "Maddest Ever Emperors".

Now that, we can do.

Our secret sauce
================

Managing collections is our secret sauce.  

As long as we have the collection in our format, we can handle pretty
much anything else.

A collection has a low probability of changing "meaning".  A textbook
on particle physics will stay a text book on particle physics.  Even
after we discover Einstein made it all up after a drunken Xmas party
at the Patent Office.

So, giving a collection a UUID does make sense, as we can be pretty 
sure that it will keep a coherency and meaning through time.

And if we keep a tree of the contents in that collections doc, then we
know which versions of modules we should retrieve in order to display
the complete collection.

We can then keep an archive (in the collection doc itself) of the previous 
tree(s).  This gives us history.



QUestions
---------

FOrmat of HTML5 module.
  DOes it start <hml>?

What about people branching collections.  Won't we just have the same prolems
Well, yes.

