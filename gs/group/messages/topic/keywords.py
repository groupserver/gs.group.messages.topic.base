# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from gs.group.base import GroupViewlet
from queries import TopicQuery


class Keywords(GroupViewlet):

    def __init__(self, group, request, view, manager):
        super(Keywords, self).__init__(group, request, view, manager)

    @Lazy
    def keywords(self):
        tq = TopicQuery()
        # --=mpj17=-- self.view is the Viewlet Manager, self.view.view is the
        # Topic page.
        topicId = self.view.view.topicId
        retval = tq.topic_keywords(topicId)
        assert type(retval) == list
        return retval
