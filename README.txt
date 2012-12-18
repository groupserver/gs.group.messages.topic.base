Introduction
============

A *topic* is the core of the system that displays posts in GroupServer_.
It is, at its most basic, a group of posts with a common subject. This
product supplies the page for rendering the topic, the code for handling
the traversal to the topic using ``messages/topic/``, and the AJAX 
system that allows a topic to become *sticky*.

The actual rendering of each post is done by the 
``gs.group.messages.post`` product.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.messages.topic
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
