# coding=utf-8
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.app.pagetemplate import ViewPageTemplateFile
from Products.XWFCore.XWFUtils import get_user, get_user_realnames
from gs.group.base.contentprovider import GroupContentProvider

class GSStickyTopicToggleContentProvider(GroupContentProvider):
    def __init__(self, context, request, view):
        GroupContentProvider.__init__(self, context, request, view)
        self.__updated = False
          
    def update(self):
        self.__updated = True
          
        stickyTopics = self.view.get_sticky_topics()
        stickyTopicIds = [topic['topic_id'] for topic in stickyTopics]
        # Add or remove the topic.
        self.add = self.topicId not in stickyTopicIds
          
    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        self.pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)

        addOrRemove = self.add and 'add' or 'remove'
        return self.pageTemplate(instance=addOrRemove,
                                   add=self.add,
                                   groupId=self.groupInfo.get_id(),
                                   siteId=self.siteInfo.get_id(),
                                   topicId=self.view.topicId)
          
    #########################################
    # Non standard methods below this point #
    #########################################

