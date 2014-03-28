# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals
SUBSYSTEM = 'gs.group.messages.topic'
from logging import getLogger
log = getLogger(SUBSYSTEM)
from zope.component import getMultiAdapter
from gs.group.base.page import GroupPage
from .error import NoIDError, Hidden


class GSTopicTraversal(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

    def publishTraverse(self, request, name):
        # Topics are identified by the post ID. This allows the
        # "visited" state of topic-links to change.
        if ('postId' not in self.request):  # TODO: check that this works!!
            self.request['postId'] = name
        return self

    def __call__(self):
        try:
            retval = getMultiAdapter((self.context, self.request),
                                        name="gstopic")()
        except NoIDError as n:
            uri = '%s/messages/topics.html' % self.groupInfo.url
            m = 'No post ID in <%s>. Going to <%s>' % \
                (self.request.URL, uri)
            log.info(m)
            log.info(n)
            retval = self.request.RESPONSE.redirect(uri)
        except Hidden as h:
            m = 'Not showing the hidden topic <%s>' % self.request.URL
            log.info(m)
            log.info(h)
            retval = getMultiAdapter((self.context, self.request),
                        name="topic_hidden.html")()
        return retval
