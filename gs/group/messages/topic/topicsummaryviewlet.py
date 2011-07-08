# coding=utf-8
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet

class TopicSummary(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = self.view.topic
        return retval

