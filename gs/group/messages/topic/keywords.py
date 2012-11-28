# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet


class Keywords(GroupViewlet):

    def __init__(self, group, request, view, manager):
        super(Keywords, self).__init__(group, request, view, manager)

    @Lazy
    def keywords(self):
        retval = []
        assert type(retval) == list
        return retval
