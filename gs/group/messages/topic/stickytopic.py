# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.group.base.page import GroupPage
from .queries import TopicQuery


class StickyPage(GroupPage):
    @Lazy
    def topicQuery(self):
        retval = TopicQuery(self.context)
        return retval


class StickyGetter(StickyPage):

    def __init__(self, virtualMailingListFolder, request):
        StickyPage.__init__(self, virtualMailingListFolder, request)
        self.topicId = request.get('topicId', None)

        response = self.request.response
        response.setHeader(to_ascii("Content-Type"),
                            to_ascii('text/plain; charset=UTF-8'))
        filename = '%s-%s-%s-get.txt' % (self.siteInfo.id,
                                            self.groupInfo.id,
                                            self.topicId)
        response.setHeader(to_ascii('Content-Disposition'),
                            to_ascii('inline; filename="%s"' % filename))

    def __call__(self):
        if self.topicQuery.topic_sticky(self.topicId):
            retval = '1'
        else:
            retval = '0'
        return retval.encode('UTF-8')


class StickySetter(StickyPage):

    def __init__(self, virtualMailingListFolder, request):
        StickyPage.__init__(self, virtualMailingListFolder, request)
        self.topicId = request.get('topicId', None)

        response = self.request.response
        response.setHeader(to_ascii("Content-Type"),
                            to_ascii('text/plain; charset=UTF-8'))
        filename = '%s-%s-%s-set.txt' % (self.siteInfo.id,
                                            self.groupInfo.id,
                                            self.topicId)
        response.setHeader(to_ascii('Content-Disposition'),
                            to_ascii('inline; filename="%s"' % filename))

    def __call__(self):
        s = self.request.get('sticky', None)
        sticky = s == '1'
        self.topicQuery.set_sticky(self.topicId, sticky)
        return '-1'.encode('UTF-8')
