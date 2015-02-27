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
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from zope.schema import (Bytes, Choice, Text, TextLine)
from . import GSMessageFactory as _


class ITopicPage(IViewletManager):
    '''A viewlet manager for the topic page'''


class ITopicSummary(IViewletManager):
    '''A viewlet manager for the topic summary'''


class ITopicFreeformSummary(IViewletManager):
    '''A viewlet manager for the topic summary'''


class ITopicTasks(IViewletManager):
    '''A viewlet manager for the topic tasks function'''


class ITopicJavaScript(IViewletManager):
    '''A viewlet manager for the JavaScript on the topic page'''


class IGSPostMessage(Interface):
    fromAddress = Choice(
        title=_('from-address', 'Email from'),
        description=_('from-address-help',
                      'The email address that you want in the "From" '
                      'line in the email you send.'),
        vocabulary='EmailAddressesForLoggedInUser',
        required=True)

    message = Text(
        title=_('message', 'Message'),
        description=_('message-help',
                      'The message you want to post to this topic.'),
        required=True)

    uploadedFile = Bytes(
        title='Files',
        description='A file you wish to add.',
        required=False)


class IGSAddToTopicFields(IGSPostMessage):
    '''Fields used on the topic page.'''
    inReplyTo = TextLine(
        title='In Reply To Identifier',
        description='The ID of the most recent post to the topic',
        required=True)
