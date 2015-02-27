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
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFFileLibrary2.hidden import FileHidden


class TopicHidden(FileHidden):
    index = ZopeTwoPageTemplateFile('browser/templates/topic.pt')

    def __init__(self, context, request):
        request.form['q'] = request.URL
        request.form['f'] = request['postId']
        FileHidden.__init__(self, context, request)
