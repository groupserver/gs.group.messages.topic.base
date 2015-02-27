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


class SummaryStats(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        super(SummaryStats, self).__init__(messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = [post for post in self.view.topic if not(post['hidden'])]
        return retval

    @Lazy
    def length(self):
        retval = len(self.topic)
        return retval

    @Lazy
    def lenAuthors(self):
        aIds = set([post['author_id'] for post in self.topic])
        retval = len(aIds)
        return retval
