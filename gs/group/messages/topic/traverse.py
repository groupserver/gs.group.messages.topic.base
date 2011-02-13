# coding=utf-8
from traceback import format_exc
from zope.component import getMultiAdapter
from zope.location.interfaces import LocationError
from zope.publisher.interfaces import NotFound
from gs.group.base.page import GroupPage
# from error import NoIDError

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
        except Exception, e:
            self.request.form['q'] = self.request.URL
            self.request.form['m'] = format_exc()
            log.error(format_exc())
            retval = getMultiAdapter((self.context, self.request),
                        name="new_unexpected_error.html")()
        return retval

