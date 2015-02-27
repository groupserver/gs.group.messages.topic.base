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
from gs.group.privacy.interfaces import IGSGroupVisibility
from gs.group.base import GroupViewlet


class ShareBar(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        super(ShareBar, self).__init__(messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = [post for post in self.view.view.topic]
        return retval

    @Lazy
    def topicName(self):
        retval = self.view.view.topicName
        return retval

    @Lazy
    def url(self):
        lastPost = self.topic[-1]
        retval = '%s/r/topic/%s' % (self.siteInfo.url, lastPost['post_id'])
        assert retval
        return retval

    @Lazy
    def isPublic(self):
        vis = IGSGroupVisibility(self.groupInfo)
        retval = vis.isPublic
        return retval
