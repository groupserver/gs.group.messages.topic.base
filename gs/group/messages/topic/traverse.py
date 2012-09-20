# coding=utf-8
from zope.component import getMultiAdapter
from gs.group.base.page import GroupPage
from error import NoIDError, Hidden

SUBSYSTEM = 'gs.group.messages.topic'
import logging
log = logging.getLogger(SUBSYSTEM)


class GSTopicTraversal(GroupPage):
    def __init__(self, context, request):
        GroupPage.__init__(self, context, request)

    def publishTraverse(self, request, name):
        # Topics are identified by the post ID. This allows the
        # "visited" state of topic-links to change.
        if ('postId' not in self.request):  # TODO: check that this works!!
            self.request['postId'] = name
        return self

    def __call__(self):
        try:
            retval = getMultiAdapter((self.context, self.request),
                                        name="gstopic")()
        except NoIDError, n:
            uri = '%s/messages/topics.html' % self.groupInfo.url
            m = 'No post ID in <%s>. Going to <%s>' % \
                (self.request.URL, uri)
            log.info(m)
            log.info(n)
            retval = self.request.RESPONSE.redirect(uri)
        except Hidden, h:
            m = 'Not showing the hidden topic <%s>' % self.request.URL
            log.info(m)
            log.info(h)
            retval = getMultiAdapter((self.context, self.request),
                        name="topic_hidden.html")()
        return retval
