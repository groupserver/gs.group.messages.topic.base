# coding=utf-8
from zope.security.interfaces import Unauthorized
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter, createObject
from zope.interface import implements
from zope.formlib import form
from zope.publisher.interfaces import NotFound
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.GSGroupMember.groupmembership import user_admin_of_group
from Products.XWFMailingListManager.queries import MessageQuery
from Products.XWFMailingListManager.addapost import add_a_post
from gs.group.base.form import GroupForm
from gs.group.member.canpost.interfaces import IGSPostingUser
from gs.profile.email.base.emailuser import EmailUser
from interfaces import IGSAddToTopicFields
from error import NoIDError

class GSTopicView(GroupForm):
    """View of a single GroupServer Topic"""
    label = u'Topic View'
    pageTemplateFileName = 'browser/templates/topic.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSAddToTopicFields, render_context=False)
    
    def __init__(self, context, request):
        GroupForm.__init__(self, context, request)
        self.postId = self.request.get('postId', None)
        if not self.postId:
            raise NoIDError('No ID Specified')
        
        self.__stickyTopics = self.__topic = self.__inReplyTo = None

    def setUpWidgets(self, ignore_request=True):
        self.adapters = {}
        if self.userInfo.anonymous:
            fromAddr = ''
        else:
            emailUser = EmailUser(self.context, self.userInfo)
            addrs = emailUser.get_delivery_addresses()
            if addrs:
                fromAddr = addrs[0]
            else:
                fromAddr = ''
        data = {
          'fromAddress': fromAddr,
          'message':     u'',
          'sticky':      self.topicSticky,
          'inReplyTo':   self.lastPostId,
        }
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)
        assert self.widgets
        
    @form.action(label=u'Add', failure='handle_action_failure')
    def handle_add(self, action, data):
      if self.__inReplyTo != data['inReplyTo']:
          # --=mpj17=-- Formlib sometimes submits twice submits twice
          self.__inReplyTo = data['inReplyTo']
          uploadedFiles = [self.request[k] 
                           for k in self.request.form 
                           if (('form.uploadedFile' in k) and 
                                self.request[k])]
          
          r = add_a_post(
            groupId=self.groupInfo.id, 
            siteId=self.siteInfo.id, 
            replyToId=data['inReplyTo'],
            topic='Re: %s' % self.topicName, 
            message=data['message'],
            tags=[], 
            email=data['fromAddress'], 
            uploadedFiles=uploadedFiles,
            context=self.context, 
            request=self.request)
          if r['error']:
              # TODO make a seperate validator for messages that the
              #   web and email subsystems can use to verifiy the
              #   messages before posting them.
              self.status = r['message']
          else:
              self.status = u'<a href="%(id)s#(id)s">%(message)s</a>' % r
      assert self.status
      assert type(self.status) == unicode

    @form.action(label=u'Change', failure='handle_action_failure')
    def handle_add_to_sticky(self,action, data):
        if data['sticky']:
            self.add_topic_to_sticky()
            self.status = u'<cite>%s</cite> has been '\
              u'<strong>added</strong> to the list of sticky '\
              u'topics in %s' % (self.topicName, self.groupInfo.name)
        else:
            self.remove_topic_from_sticky()
            self.status = u'<cite>%s</cite> has been '\
              u'<strong>removed</strong> from the list of sticky '\
              u'topics in %s' % (self.topicName, self.groupInfo.name)
        assert self.status
        assert type(self.status) == unicode
       
    def handle_action_failure(self, action, data, errors):
      if len(errors) == 1:
          self.status = u'<p>There is an error:</p>'
      else:
          self.status = u'<p>There are errors:</p>'

    def add_topic_to_sticky(self):
        group = self.groupInfo.groupObj
        if group.hasProperty('sticky_topics'):
            topics = self.sticky_topics
            if self.topicId not in topics:
                topics.append(self.topicId)
            group.manage_changeProperties(sticky_topics=topics)
        else:
            group.manage_addProperty('sticky_topics', [self.topicId],
                'lines')
        self.__stickyTopics == None
        assert group.hasProperty('sticky_topics')

    def remove_topic_from_sticky(self):
        group = self.groupInfo.groupObj
        if group.hasProperty('sticky_topics'):
            topics = list(group.getProperty('sticky_topics'))
            if self.topicId in topics:
                topics.remove(self.topicId)
            group.manage_changeProperties(sticky_topics=topics)
        else:
            group.manage_addProperty('sticky_topics', [], 'lines')
        self.__stickyTopics == None
        assert group.hasProperty('sticky_topics')

    @Lazy
    def userInfo(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval
        
    @Lazy
    def userPostingInfo(self):
        g = self.groupInfo.groupObj
        assert g
        # --=mpj17=-- A Pixie Caramel to anyone who can tell me
        #    why the following line does not work in Zope 2.10.
        #   "Zope Five is screwed" is not sufficient.
        #self.userPostingInfo = IGSPostingUser((g, userInfo))
        retval = getMultiAdapter((g, self.userInfo), IGSPostingUser)
        assert retval
        return retval
        
    @Lazy
    def messageQuery(self):
        da = self.context.zsqlalchemy 
        assert da, 'No data-adaptor found'
        retval = MessageQuery(self.context, da)
        assert retval
        return retval

    @Lazy
    def topicId(self):
        retval = self.messageQuery.topic_id_from_post_id(self.postId)
        if not retval:
            retval = self.topic_id_from_legacy_post_id(self.postId)
        assert retval != None
        return retval
        
    def topic_id_from_legacy_post_id(self, legacyPostId):
        p = self.messageQuery.post_id_from_legacy_id(legacyPostId)
        if not p:
          raise NotFound(self, legacyPostId, self.request)
        assert p, 'Post not found for legacy post ID (%s)' % legacyPostId
        retval = self.messageQuery.topic_id_from_post_id(p)
        assert retval, 'Topic not found for post ID (%s)' % p
        return retval
        
    @property
    def topic(self):
        # This is deliberately not a Lazy property
        if ((self.__topic == None) or self.status):
            self.__topic = self.messageQuery.topic_posts(self.topicId)
            if self.__topic[0]['group_id'] != self.groupInfo.id:
                raise Unauthorized('You are not authorized to access '\
                    'this topic in the group %s' % self.groupInfo.name)
        assert type(self.__topic) == list
        assert len(self.__topic) >= 1, \
          "No posts in the topic %s" % self.topicId
        return self.__topic
        
    @property
    def lastPostId(self):
        # This is deliberately not a Lazy property
        return self.topic[-1]['post_id']

    @Lazy
    def topicName(self):
        retval = self.topic[0]['subject']
        assert retval
        return retval
    
    @Lazy
    def nextTopic(self):
        r = self.messageQuery.later_topic(self.topicId)
        if r:
            retval = TopicInfo(r['last_post_id'], r['subject'])
        else:
            retval = TopicInfo(None,None)
        assert retval != None
        return retval
        
    @Lazy
    def previousTopic(self):
        r = self.messageQuery.earlier_topic(self.topicId)
        if r:
            retval = TopicInfo(r['last_post_id'], r['subject'])
        else:
            retval = TopicInfo(None,None)
        assert retval
        return retval

    @property
    def topicSticky(self):
        # This is deliberately not a Lazy property
        retval = self.topicId in self.sticky_topics
        assert type(retval) == bool
        return retval

    @property
    def sticky_topics(self):
        # This is deliberately not a Lazy property
        retval = self.groupInfo.get_property('sticky_topics', [])
        if type(retval) != list:
            retval = list(retval)
        self.__stickyTopics = retval
        assert retval != None
        assert type(retval) == list
        return retval

    @Lazy
    def userIsAdmin(self):
        return user_admin_of_group(self.userInfo, self.groupInfo)

class TopicInfo(object):
    def __init__(self, topicId, subject):
        self.topicId = topicId
        self.subject = subject

