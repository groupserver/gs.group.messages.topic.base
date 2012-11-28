# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet


class NavLinks(GroupViewlet):
    def __init__(self, group, request, view, manager):
        GroupViewlet.__init__(self, group, request, view, manager)

    @Lazy
    def previousTopic(self):
        retval = self.view.previousTopic
        return retval

    @Lazy
    def nextTopic(self):
        retval = self.view.nextTopic
        return retval
