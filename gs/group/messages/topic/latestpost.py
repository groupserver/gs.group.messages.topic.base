# coding=utf-8
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from gs.group.privacy.interfaces import IGSGroupVisibility
from gs.group.base.viewlet import GroupViewlet

class LatestPost(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def topic(self):
        retval = [post for post in self.view.topic 
                  if not(post['hidden'])]
        return retval

    @Lazy
    def relativeUrl(self):
        lastPost = self.topic[-1]
        retval = '%s/messages/topic/%s#post-%s' % \
            (self.groupInfo.relativeURL, lastPost['post_id'], 
                lastPost['post_id'])
        return retval
        
    @Lazy
    def authorInfo(self):
        lastPost = self.topic[-1]
        authorId = lastPost['author_id']
        retval = createObject('groupserver.UserFromId', self.context, 
                                authorId)
        return retval

    @Lazy
    def lastPostDate(self):
        retval = self.topic[-1]['date']
        return retval

