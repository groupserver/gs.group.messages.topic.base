# coding=utf-8
from zope.component import createObject
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from gs.group.privacy.interfaces import IGSGroupVisibility
from gs.group.base.viewlet import GroupViewlet


class PostList(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = self.view.topic
        return retval

    @Lazy
    def topicName(self):
        retval = self.view.topicName
        return retval

    @Lazy
    def isPublic(self):
        vis = IGSGroupVisibility(self.groupInfo)
        return vis.isPublic

