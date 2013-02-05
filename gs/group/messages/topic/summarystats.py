# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet


class SummaryStats(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

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
