# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter, createObject
from gs.group.base.page import GroupPage
from queries import TopicQuery

class StickyPage(GroupPage):
    @Lazy
    def topicQuery(self):
        retval = TopicQuery(self.context)
        return retval

class StickyGetter(StickyPage):

    def __init__(self, virtualMailingListFolder, request):
        StickyPage.__init__(self, virtualMailingListFolder, request)
        self.topicId = request.get('topicId', None)
        
        response = self.request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = '%s-%s-%s-get.txt' % (self.siteInfo.id, 
                                            self.groupInfo.id, 
                                            self.topicId)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
    
    def __call__(self):
        if self.topicQuery.topic_sticky(self.topicId):
            retval = u'1'
        else:
            retval = u'0'
        return retval.encode('UTF-8')

class StickySetter(StickyPage):

    def __init__(self, virtualMailingListFolder, request):
        StickyPage.__init__(self, virtualMailingListFolder, request)
        self.topicId = request.get('topicId', None)
        
        response = self.request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = '%s-%s-%s-set.txt' % (self.siteInfo.id, 
                                            self.groupInfo.id, 
                                            self.topicId)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
    
    def __call__(self):
        sticky = self.request.get('sticky', None) == '1'
        self.topicQuery.set_sticky(self.topicId, sticky)
        return u'-1'.encode('UTF-8')

