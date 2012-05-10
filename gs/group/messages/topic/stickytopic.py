# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter, createObject
from gs.group.base.page import GroupPage

class StickyGetter(GroupPage):

    def __init__(self, virtualMailingListFolder, request):
        GroupPage.__init__(self, virtualMailingListFolder, request)
        self.topicId = request.get('topicId', None);
        
        response = self.request.response
        response.setHeader("Content-Type", 'text/plain; charset=UTF-8')
        filename = '%s-%s-%s-status.txt' % (self.siteInfo.id, 
                                            self.groupInfo.id, 
                                            self.topicId)
        response.setHeader('Content-Disposition',
                            'inline; filename="%s"' % filename)
    
    def __call__(self):
        return u'-1'.encode('UTF-8')

