=========
Use cases
=========

This is a discussion about the likely use cases for the
editor/repository combination and then links into a expected API
design to allow the use cases to be supported, and also discusses the
likely technology choices.


U1. Simplest possible use case
------------------------------

Professor Aardvark is the current holder of the Simon Cowell Chair for
the Public Appreciation of Music and wishes to write the definitive
work on the history of 80's band A Flock of Seagulls, soon to be
required reading for all Freshmen at MIT.

He decides to publish it through Connexions and creates an account at
cnx.org (username: bighaircut).

He uses his personal workspace, and the EIP editor, and creates
chapter after chapter, words flowing from him as if he was reading
from inside his own skull.  He never corrects any saved work and never
needs to go back and re-edit.

After 20 chapters, he stops.  

He needs to link all the 20 modules / chapters into one book.

He does this by 

1. clicking create a book in his workspace home page. and entering in
   the book title 'Flocking good music'.  The workspace home page is
   divided into two - the left is modules, a long unsorted list of
   work he has done, and their versions.  The right hand side is a set
   of books (collections) - each expandable into a sorted list of
   modules (i.e. chapters)

2. dragging modules from his workspace into the correct collection on
   the RHS, and the chapters then appear in the book underneath the
   previous chapter.

3. He then clicks 'proof-read' - and can see an HTML version of the
   book in a pop up window.

He proof reads the whole book, and finds just one spelling mistake ("I
rum away" (!)).

He opens his workspace again, locates the chapter in the collection,
and opens the module in the editor by clicking 'edit' next to the
chapter name.

He changes the spelling mistake (Chortling that he could get something
so obvious wrong) and presses 'save'.

Now the book is at version 1, all chapters apart from chapter 9 is at
version 1 and chapter 9 (with the spelling mistake corrected) is
version 2.

He clicks 'freeze book' - which tags the book collection at the
current versions.

And he publishes the frozen version.  The pdf looks great, and it soon
rises to the top of the cnx.org bestseller list.

U2. Simple Editing
------------------

'Simon just loves it Dahling'.  Our Professor is overjoyed and decides
that his dry prose could be enlivened with some photos.  He digs
through his sock drawer and finds his old kodak-color prints of the
amazing '83 concert.  After scanning in all 24 of them, he creates an
entirely new chapter in his workspace, imports each photo and lovingly
adds a caption, and then in the collection view, he drags it over to
the right place in the list of chapters.

He freezes the new book and publishes.

Like Hotcakes.  No, seriously, people are lapping it up.


U3. Rearranging chapter order
-----------------------------

But there is a problem now.  

Professor A wants to re-emphasise the vital role that videos played in
the band's development, and the America billboard smash.  And he cannot
do this with 20 chapters.

He thinks he needs to split out many chapters into different parts and
re-arrange them - but he does not want to muck about too much as he is
planning to make every instance of a band members name UPPERCASE, and
is only part way through that.

He needs to branch.

This can be represented as a new workspace - he just checkouts a workspace,
and it is a new branch, he names it 'video-version'.



U4. Bringing in someone else's work
-----------------------------------

Professor A decides it is time to pull in the remarkable work of
leading music critic T.I. Near and his world famous, Word doc. of 
band reviews.

Professor clicks 'create new module from word doc', enters the URL of
the word doc, and imports it into his workspace called
'video-version'.  The word doc is converted as best as possible into
HTML5 and stored as tinear.doc.html

However, there is a problem with the doc - it has bold and normal text
only and no other styling information.

So the HTML is just <strong> and <p>

The professor very nicely goes through the document assigning a
'header' to the bold and 'section' to the paragraphs.  He then notices
the phil-o-matic tool that would have done this for him.

THe professor now drags the tinear.doc.html into the book in workspace
'video-version', just after the photo chapters.

He freezes the book in this new workspace.  He decides to publish from here -
and does so.

MTV runs a retrospective on the Professor's career.  Prime time !

U5. Working with others
-----------------------

After his triumphant appearance on Good Morning America plugging the
new book, several other promient academics emailed our Professor to
ask if they could collaborate to create the definitive encyclopaedia 
of 1980's New Romantics.

This is looking good.  He emails Professor Xavier and Professor Zoltan
and tells them to create accounts on cnx.org, and to then checkout his
workspace 'video-version' - he gives their accounts permission to do
this.

They are 'authors' roles and he is a 'editor' role

Unfortunately both Professors edit the skeleton chapter 'Her Name is
Duran Duran', with Professor X writing about the origin of the name in
the film Barbarella.  But Professor Z just ranted on about Jane Fonda's
later career.  No-one mentioned the floating upside down bit.  

Both men send in 'please add to book' requests.

Clearly both chapters cannot be put into the same book - so Professer
A first reviews them - and sends back several spelling and style
corrections.  And does mention the floating upside down bit.

The men make the changes and repeat the 'add to book' request.

Professor A now has to use the merge tool to decide which parts of the
two requests will be kept and which discarded.

.. sidebar :: Help.

   (This is a difficult and trickly area.  Not sure how to approach
   this - merging HTML ! But we are merging *strucutred* html - is
   this helpful?  Comments anyone?)

U6. Outside of cnx.org
----------------------

The respected Professor Q has heard about the project and sends in his
own chapter by email.  It was created in notepad, and is valid html5 (cnxml?)

The same process as above is followed, firstly a spell check and corrections
then a merge process.

The imported document is taken using a URL.



