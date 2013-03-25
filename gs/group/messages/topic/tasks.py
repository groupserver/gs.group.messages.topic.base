# -*- coding: utf-8 -*-
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
