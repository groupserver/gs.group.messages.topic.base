# coding=utf-8
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.component import createObject
from zope.app.pagetemplate import ViewPageTemplateFile
from gs.group.base.contentprovider import GroupContentProvider
          
class GSTopicSummaryContentProvider(GroupContentProvider):
      """GroupServer Topic Simmary Content Provider: summarise a topic
      """
      post = None
      def __init__(self, context, request, view):
        GroupContentProvider.__init__(self, context, request, view)
        self.__updated = False

      def update(self):
          self.__updated = True
          self.lastPost = self.topic[-1]
          self.authorId = self.lastPost['author_id']
          self.authorInfo = createObject('groupserver.UserFromId', 
            self.context, self.authorId)

          authorIds = []
          for post in self.topic:
              if post['author_id'] not in authorIds:
                  authorIds.append(post['author_id'])
          self.lenAuthors = len(authorIds)
          assert self.__updated
          
      def render(self):
          if not self.__updated:
              raise UpdateNotCalled
      
          pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)          

          return pageTemplate(self, length=len(self.topic),
                              lenAuthors=self.lenAuthors,
                              lastPostId = self.lastPost['post_id'],
                              lastPostDate = self.lastPost['date'],
                              authorInfo=self.authorInfo, 
                              context=self.context,
                              siteName = self.siteInfo.get_name(),
                              siteURL = self.siteInfo.get_url(),
                              groupId = self.groupInfo.get_id())

      #########################################
      # Non-standard methods below this point #
      #########################################
          

      def user_authored(self):
          """Did the user write the email message?
          
          ARGUMENTS
              None.
          
          RETURNS
              A boolean that is "True" if the current user authored the
              email message, "False" otherwise.
              
          SIDE EFFECTS
              None."""
          assert self.lastPost
          assert self.request
          assert self.authorId
          
          user = self.request.AUTHENTICATED_USER
          retval = user.getId() == self.authorId
          
          assert retval in (True, False)
          return retval

