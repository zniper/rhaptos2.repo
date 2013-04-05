=========================
Backbone model validation
=========================

The tests in repo/tests/js are designed to ensure that a backbone.js model
is valid when run against the API in repo.

This seems a sensible way to ensure that changes are caught *by the same person who changed the repo* 



What is backbone?
=================

I did not expect to put this here, but the `intro <http://backbonejs.org/>`_ from the site is sooo good its worth repeating::

    When working on a web application that involves a lot of JavaScript, one of
    the first things you learn is to stop tying your data to the DOM. It's all
    too easy to create JavaScript applications that end up as tangled piles of
    jQuery selectors and callbacks, all trying frantically to keep data in sync
    between the HTML UI, your JavaScript logic, and the database on your
    server. For rich client-side applications, a more structured approach is
    often helpful.

    With Backbone, you represent your data as Models, which can be created,
    validated, destroyed, and saved to the server. Whenever a UI action causes
    an attribute of a model to change, the model triggers a "change" event; all
    the Views that display the model's state can be notified of the change, so
    that they are able to respond accordingly, re-rendering themselves with the
    new information. In a finished Backbone app, you don't have to write the
    glue code that looks into the DOM to find an element with a specific id, and
    update the HTML manually — when the model changes, the views simply update
    themselves.



