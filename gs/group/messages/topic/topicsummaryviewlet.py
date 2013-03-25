# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet


class TopicSummary(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = self.view.topic
        return retval
