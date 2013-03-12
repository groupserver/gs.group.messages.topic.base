===========================
``gs.group.messages.topic``
===========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Topic page for a GroupServer Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-03-12
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

A *topic* is the core of the system that displays posts in GroupServer_.
It is, at its most basic, a group of posts with a common subject. This
product supplies the code for handling the traversal_ to the topic, and the
page_ for rendering the topic.

Traversal
=========

The ``messages/topic`` traversal system is used to determine if a
participant should see the topic page_, a ``410 Gone`` error page (if the
topic has been hidden), or a ``404 Not Found`` if the topic does not exist.

Page
====

The *Topic Page* is the workhorse of GroupServer, as it displays the core
content of a GroupServer group. It is divided into four main sections: a
summary_ a sticky_ toggle, the `list of posts`_ itself, and the `Post a
reply`_ form. Most sections provide viewlets for the
``gs.group.messages.topic.interfaces.ITopicPage`` viewlet manager.

Summary
-------

The *Topic Page* starts with a summary of the topic: how many posts, who
made the most recent post, and the keywords. This summary is designed to
reflect the metadata shown in the Topics list on the Group page.

Sticky
------

The sticky-topic toggle appears as part of the toolbar at the top of the
*Topic Page*, next to the navigation links and the Share button, if the
person that is viewing the page is an administrator. The toggle is a small
form, provided by the ``gs-group-messages-topic-admin-stickytoggle``
viewlet. When the page is loaded it checks with page
``gs-group-messages-topic-sticky-getter`` to determine if the topic is
sticky or not, and adjusts the *Sticky* button accordingly. When the
administrator toggles the *Sticky* button the page
``gs-group-messages-topic-sticky-setter`` is used to change the topic.

List of Posts
-------------

The list of posts, provided by the ``gs-group-messages-topic-list``
viewlet, forms the bulk of the *Topic Page*. However, the list is simple,
as most of the actual rendering of each post in the topic is done by the
``gs.group.messages.post`` product.

Post a Reply
------------

The *Topic Page* finishes with the *Post a reply* form. It is shown to
everyone that can post (determined by ``gs.group.member.canpost``). It is a
non-stand form: 

* The ``From`` field uses the user's name and profile photo in place of a
  label.

* The ``Message`` field is unlabelled.

* The multi-file widget (provided by ``gs.content.js.multifile``) enables
  an arbitrary number of widgets to be submitted with the form.

The lack of labels makes the *Post a reply* form more similar to a standard
email client.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.messages.topic
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/
