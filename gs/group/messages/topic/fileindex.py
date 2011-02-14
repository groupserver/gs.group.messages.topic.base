# coding=utf-8
from zope.contentprovider.interfaces import UpdateNotCalled
from zope.app.pagetemplate import ViewPageTemplateFile
from Products.XWFCore.XWFUtils import get_user, get_user_realnames
from gs.group.base.contentprovider import GroupContentProvider

class GSFileIndexContentProvider(GroupContentProvider):
    def __init__(self, context, request, view):
        GroupContentProvider.__init__(self, context, request, view)
        self.__updated = False
      
    def update(self):
        # The entries list is made up of 4-tuples representing the
        #   post ID, files, author, user authored, and post-date.
        hr = self.view.topic[-1]['post_id']
        self.entries = [{'href':  '%s#post-%s' % (hr, post['post_id']),
                     'files': self.get_file_from_post(post),
                     'name':  self.get_author_realnames_from_post(post),
                     'user':  self.get_user_authored_from_post(post),
                     'date':  self.get_date_from_post(post)} 
                     for post in self.view.topic ]
        self.nPosts = sum([1 for e in self.entries if e['files']])
        self.nFiles = sum([len(e['files']) for e in self.entries])
        self.show = self.nFiles > 0
              
        self.__updated = True
          
    def render(self):
        if not self.__updated:
          raise UpdateNotCalled

        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        return pageTemplate(self, entries=self.entries, 
            context=self.context)
          
    #########################################
    # Non standard methods below this point #
    #########################################
      
    def get_author_realnames_from_post(self, post):
        """Get the names of the post's author.

        ARGUMENTS
          "post" A post object.
          
        RETURNS
          The name of the post's author. 

        SIDE EFFECTS
         None.
        """
        assert post

        authorId = post['author_id']
        retval = get_user_realnames(get_user(self.context, authorId))

        return retval
          
    def get_user_authored_from_post(self, post):
        """Did the user write the email message?

        ARGUMENTS
          None.

        RETURNS
          A boolean that is "True" if the current user authored the
          email message, "False" otherwise.
          
        SIDE EFFECTS
          None."""
        assert post
        assert self.request

        user = self.request.AUTHENTICATED_USER
        retval = user.getId() == post['author_id']

        assert retval in (True, False)
        return retval

    def get_date_from_post(self, post):
        assert post
        retval = post['date']
        assert retval
        return retval
      
    def get_file_from_post(self, post):
        retval = []
        if post['files_metadata']:
          retval = post['files_metadata']
        return retval

