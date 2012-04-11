Dev guidelines
==============

1. We shall use the Bezos SOA `approach <https://plus.google.com/110981030061712822816/posts/AaygmbzVeRq>`_ - nothing, absolutely nothing communicates with anything else except through defined agreed service APIs - basically, use http.

1.a. This has an implication for testing.  The first division in tests is not unit vs functional, but internal to the 'service' and external.  Internal tests are allowed to know something about the inner workings, allowed to go peak at the disk to see if the file actually got written.  External ones, no.  Just use the API and test what comes back.. Test it hard. Throw horrible edge cases, drop connections.  But no peaking.

