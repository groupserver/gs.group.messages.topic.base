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
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet
from gs.group.messages.privacy import MessagesPrivacy
# TODO: Move all post-creation code to gs.group.messages.add.base
# TODO: Convert to z3c.form.
# TODO: Make this a sub-form.
#   http://pypi.python.org/pypi/z3c.form#sub-forms


class AddToTopic(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def show(self):
        postingInfo = self.view.userPostingInfo
        assert postingInfo
        retval = postingInfo.canPost
        return retval

    @Lazy
    def topicName(self):
        retval = self.view.topicName
        return retval

    @Lazy
    def widgets(self):
        retval = self.view.widgets
        return retval

    @Lazy
    def visibleWidgets(self):
        retval = [self.view.widgets['fromAddress'],
                  self.view.widgets['message']]
        return retval

    @Lazy
    def hiddenWidgets(self):
        retval = [self.view.widgets['inReplyTo']]
        return retval

    @Lazy
    def availableActions(self):
        retval = self.view.availableActions
        return retval

    @Lazy
    def privacy(self):
        retval = MessagesPrivacy(self.context)
        return retval
