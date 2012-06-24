# coding=utf-8
from traceback import format_exc
from zope.component import getMultiAdapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces import NotFound
from gs.group.base.page import GroupPage
from error import NoIDError, Hidden

SUBSYSTEM = 'gs.group.messages.topic'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

class GSTopicTraversal(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)
        
    def publishTraverse(self, request, name):
        # Topics are identified by the post ID. This allows the 
        # "visited" state of topic-links to change.
        if not self.request.has_key('postId'):
            self.request['postId'] = name
        return self
        
    def __call__(self):
        try:
            retval = getMultiAdapter((self.context, self.request), name="gstopic")()
        except NoIDError, n:
            uri = '%s/messages/topics.html' % self.groupInfo.url
            m = 'No post ID in <%s>. Going to <%s>' % \
                (self.request.URL, uri)
            log.info(m)
            retval = self.request.RESPONSE.redirect(uri)
        except Hidden, h:
            retval = getMultiAdapter((self.context, self.request),
                        name="topic_hidden.html")()
        return retval

