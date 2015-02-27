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


class TasksViewlet(GroupViewlet):
    def __init__(self, group, request, view, manager):
        super(TasksViewlet, self).__init__(group, request, view, manager)

    @property
    def topic(self):
        retval = getattr(self.view, 'topic')
        return retval

    @Lazy
    def previousTopic(self):
        # TODO: Figure out why getattr is needed
        retval = getattr(self.view, 'previousTopic')
        return retval

    @Lazy
    def nextTopic(self):
        retval = getattr(self.view, 'nextTopic')
        return retval
