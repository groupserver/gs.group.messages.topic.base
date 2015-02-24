================================
``gs.group.messages.topic.base``
================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Topic page for a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-02-23
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

A *topic* is the core of the system that displays posts in
GroupServer_.  It is, at its most basic, a group of posts with a
common subject. This product supplies the code for handling the
traversal_ to the topic, the page_ for rendering the topic, and
some supporting JavaScript_.

Traversal
=========

The ``messages/topic`` traversal system is used to determine if a
participant should see the topic page_, a ``410 Gone`` error page
(if the topic has been hidden), or a ``404 Not Found`` if the
topic does not exist.

Page
====

The *Topic Page* is the workhorse of GroupServer, as it displays
the core content of a GroupServer group. It is divided into four
main sections: a summary_ a sticky_ toggle, the `list of posts`_
itself, and the `Post a reply`_ form. Most sections provide
viewlets for the
``gs.group.messages.topic.base.interfaces.ITopicPage`` viewlet
manager.

Summary
-------

The *Topic Page* starts with a summary of the topic: how many
posts, who made the most recent post, and the keywords. This
summary is designed to reflect the metadata shown in the Topics
list on the Group page.

Sticky
------

The sticky-topic toggle appears as part of the toolbar at the top
of the *Topic Page*, next to the navigation links and the Share
button, if the person that is viewing the page is an
administrator. The toggle is a small form, provided by the
``gs-group-messages-topic-admin-stickytoggle`` viewlet. When the
page is loaded it checks with page
``gs-group-messages-topic-sticky-getter`` to determine if the
topic is sticky or not, and adjusts the *Sticky* button
accordingly. When the administrator toggles the *Sticky* button
the page ``gs-group-messages-topic-sticky-setter`` is used to
change the topic.

List of Posts
-------------

The list of posts, provided by the
``gs-group-messages-topic-list`` viewlet, forms the bulk of the
*Topic Page*. However, the list is simple, as most of the actual
rendering of each post in the topic is done by the
``gs.group.messages.post`` product [#post]_.

Post a Reply
------------

The *Topic Page* finishes with the *Post a reply* form. It is
shown to everyone that can post [#canpost]_. It is a non-stand
form:

* The ``From`` field uses the user's name and profile photo in
  place of a label.
* The ``Message`` field is unlabelled.
* The multi-file widget [#multifile]_ enables an arbitrary number
  of widgets to be submitted with the form.

The lack of labels makes the *Post a reply* form more similar to
a standard email client.

JavaScript
==========

Three JavaScript resources are provided by this product.

``/++resource++gs-group-messages-topic-multifile-20130201.js``:
  Customisation to the MultiFile system [#multifile]_.

``/++resource++stickytoggle-20121219.js``:
  Client-side code to power the Sticky_ toggle.

``/++resource++gs-group-messages-topic-privacy-20130201.js``: 
  Creates a Popover_ from the privacy information in the `Post a Reply`_
  form.

Resources
=========

- Code repository: https://github.com/groupserver/gs.group.messages.topic.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

.. [#post] See ``gs.group.messages.post``
           <https://github.com/groupserver/gs.group.messages.post/>

.. [#canpost] See ``gs.group.member.canpost``
              <https://github.com/groupserver/gs.group.member.canpost/>

.. [#multifile] See ``gs.content.js.multifile``
                <https://github.com/groupserver/gs.content.js.multifile/>

.. _Popover: http://twitter.github.com/bootstrap/javascript.html#popovers
..  LocalWords:  MultiFile
