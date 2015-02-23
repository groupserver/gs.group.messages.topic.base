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
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.base import GroupViewlet


class LatestPost(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        super(LatestPost, self).__init__(messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = [post for post in self.view.topic if not(post['hidden'])]
        return retval

    @Lazy
    def relativeUrl(self):
        retval = ''
        if self.topic:
            lastPost = self.topic[-1]
            url = '{groupUrl}/messages/topic/{lastPostId}/#post-{lastPostId}'
            retval = url.format(groupUrl=self.groupInfo.relativeURL,
                                lastPostId=lastPost['post_id'])
        return retval

    @Lazy
    def authorInfo(self):
        if self.topic:
            lastPost = self.topic[-1]
            authorId = lastPost['author_id']
        else:
            authorId = ''
        retval = createObject('groupserver.UserFromId', self.context,
                                authorId)
        return retval

    @Lazy
    def lastPostDate(self):
        retval = None
        if self.topic:
            retval = self.topic[-1]['date']
        return retval

    @Lazy
    def show(self):
        retval = len(self.topic) > 1
        return retval
