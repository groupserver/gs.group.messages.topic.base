Changelog
=========

4.0.7 (2016-10-21)
------------------

* Dropping email addresses from keywords, closing `Bug 3919`_
* Dropping URIs from keywords, closing `Bug 4028`_

.. _Bug 3919: https://redmine.iopen.net/issues/3939
.. _Bug 4028: https://redmine.iopen.net/issues/4028

4.0.6 (2016-01-28)
------------------

* Following the changes to `gs.content.js.multifile`_

.. _gs.content.js.multifile:
   https://github.com/groupserver/gs.content.js.multifile

4.0.5 (2015-11-19)
------------------

* Fixing the Hide JavaScript, so it is present in the page more often.

4.0.4 (2015-11-12)
------------------

* Following the updates to `gs.content.js.sharebox`_
* Running `gjslint`_ over the JavaScript resources

.. _gs.content.js.sharebox:
   https://github.com/groupserver/gs.content.js.sharebox
.. _gjslint:
   https://developers.google.com/closure/utilities/docs/linter_howto

4.0.3 (2015-11-10)
------------------

* Generating the topic-keywords from the most recent 127 posts,
  rather than from the entire topic

4.0.2 (2015-10-14)
------------------

* [EN] Using *Older* and *Newer* for the navigation buttons
* [DE] Adding a German translation, thanks to Cousin Clara
* Following the changes to `gs.group.messages.post.base`_

.. _gs.group.messages.post.base:
   https://github.com/groupserver/gs.group.messages.post.base

4.0.1 (2015-03-11)
------------------

* [FR] Adding a French translation, thanks to `Razique Mahroua`_

.. _Razique Mahroua:
   https://www.transifex.com/accounts/profile/Razique/

4.0.0 (2015-02-23)
------------------

* Renaming the product `gs.group.messages.topic.base`_
* Adding Transifex_ support

.. _Transifex:
   https://www.transifex.com/projects/p/gs-group-messages-topic-base/
.. _gs.group.messages.topic.base:
   https://github.com/groupserver/gs.group.messages.topic.base

3.3.1 (2014-05-13)
------------------

* ASCII fix

3.3.0 (2014-03-27)
------------------

* Following the changes to the *Share* JavaScript
* Following the changes to the *Hide* JavaScript
* Switching to *strict* mode for the sticky-topic toggle

3.2.7 (2014-02-20)
------------------

* Ensuring the headers are ``ASCII``

3.2.6 (2014-01-20)
------------------

* Updating the *fragment identifier* in the link to the last post
* String-formatting cleanup

3.2.5 (2013-12-06)
------------------

* Following the new *hide* JavaScript code
* Using the new *Loading* icon

3.2.4 (2013-11-14)
------------------

* Following the updated post-sharing code
* Updated the product metadata

3.2.3 (2013-05-23)
------------------

* Turning the *required widgets* interlock on
* Merging to JavaScript files into one, to save a request

3.2.2 (2013-04-25)
------------------

* Fixing the name of the *Keywords* viewlet

3.2.1 (2013-04-05)
------------------

* Added icons to the navigation links
* Added an icon to the *Share* bar
* Added icons to the breadcrumb trail

3.2.0 (2013-03-25)
------------------

* Minifying some JavaScript resources
* Following the member-viewlet code to `gs.group.member.viewlet`_

.. _gs.group.member.viewlet:
   https://github.com/groupserver/gs.group.member.viewlet

3.1.1 (2013-03-15)
------------------

* Using the new square profile-image content provider

3.1.0 (2013-02-22)
------------------

* Switching to Bootstrap_ for the popovers (including *Privacy*
  and *Hide*)
* Added WAI-ARIA accessibility attributes

.. _Bootstrap: http://getbootstrap.com/

3.0.0 (2013-01-09)
------------------

* Rewrite for the new GroupServer user-interface

  + Removed the file-list from the *Topic* page
  + Added a viewlet manage for more free-form summary data
  + Added the topic keywords to the *Topic* page
  + Redesigned *Add to topic* form

2.4.0 (2012-09-26)
------------------

* Using the full-text retrieval features of PostgreSQL to search
  the topics, and to generate the topic keywords

2.3.1 (2012-07-20)
------------------

* Following the *Add a post* code to `gs.group.messages.add.base`_

.. _gs.group.messages.add.base:
   https://github.com/groupserver/gs.group.messages.add.base

2.3.0 (2012-07-03)
------------------

* Updating the queries to ``gs.database``
* Following the *Add a post* code to ``gs.group.messages.add``


2.2.0 (2012-05-15)
------------------

* Switching to a full-page layout of the page
* Dropping the link to the *Topics* page
* Refactor of the sticky-topic code, making the toggle work with
  AJAX

2.1.0 (2012-03-09)
------------------

* Moving the last of the can-post code to
  `gs.group.member.canpost`_

2.0.1 (2011-10-25)
------------------

* Deal with hidden topics better

2.0.0 (2011-07-11)
------------------

* Massive refactor, moving most of the page into viewlets
* Moving the *Sticky topic* toggle to a form

1.2.0 (2011-06-07)
------------------

* Adding a ``:`` to the title of the *Topic* page
* Moving the can-post code to `gs.group.member.canpost`_

.. _gs.group.member.canpost:
   https://github.com/groupserver/gs.group.member.canpost

1.1.0 (2011-04-18)
------------------

* Added the *Hide post* JavaScript code
* Moved the *Topic* table here from
  `Products.XWFMailingListManager`_
* Added untested support for hiding a topic

1.0.0 (2011-02-19)
------------------

Initial version. Prior to the creation of this product the topics
were displayed by `Products.XWFMailingListManager`_

.. _Products.XWFMailingListManager:
   https://github.com/groupserver/Products.XWFMailingListManager

..  LocalWords:  Changelog viewlets Transifex
