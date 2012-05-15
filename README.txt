Introduction
============

A *topic* is the core of the system that displays posts in GroupServer.
It is, at its most basic, a group of posts with a common subject. This
product supplies the page for rendering the topic, the code for handling
the traversal to the topic using ``messages/topic/``, and the AJAX 
system that allows a topic to become *sticky*.

The actual rendering of each post is done by the 
``gs.group.messages.post`` product.

