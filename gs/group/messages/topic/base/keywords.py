# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet
from .queries import TopicQuery


class Keywords(GroupViewlet):

    def __init__(self, group, request, view, manager):
        super(Keywords, self).__init__(group, request, view, manager)

    @Lazy
    def keywords(self):
        tq = TopicQuery()
        # --=mpj17=-- self.view is the Viewlet Manager, self.view.view is
        # the Topic page.
        topicId = self.view.view.topicId
        retval = tq.topic_keywords(topicId)
        assert type(retval) == list
        return retval
