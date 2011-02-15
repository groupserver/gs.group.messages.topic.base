# coding=utf-8
from zope.security.interfaces import Unauthorized
from zope.component import getMultiAdapter, createObject
from zope.interface import implements
from zope.formlib import form
from zope.publisher.interfaces import NotFound
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.GSGroupMember.interfaces import IGSPostingUser
from Products.GSGroupMember.groupmembership import user_admin_of_group
from Products.XWFMailingListManager.queries import MessageQuery
from Products.XWFMailingListManager.addapost import add_a_post
from Products.GSGroup.utils import is_public
from gs.group.base.form import GroupForm
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
        
        self.isPublic = is_public(self.groupInfo.groupObj)
        
        self.__userInfo = self.__userPostingInfo = None
        self.__topicId = self.__topicName = self.__nextTopic = None
        self.__previousTopic = self.__stickyTopics = self.__topic = None
        self.__inReplyTo = self.__messageQuery = None

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
            topics = self.get_sticky_topics()
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

    @property
    def userInfo(self):
        if self.__userInfo == None:
            self.__userInfo = createObject('groupserver.LoggedInUser', 
              self.context)
        return self.__userInfo
        
    @property
    def userPostingInfo(self):
        if self.__userPostingInfo == None:
            g = self.groupInfo.groupObj
            assert g
            # --=mpj17=-- A Pixie Caramel to anyone who can tell me
            #    why the following line does not work in Zope 2.10.
            #   "Zope Five is screwed" is not sufficient.
            #self.userPostingInfo = IGSPostingUser((g, userInfo))
            self.__userPostingInfo = getMultiAdapter((g, self.userInfo), 
                                                      IGSPostingUser)
        assert self.__userPostingInfo
        return self.__userPostingInfo
        
    @property
    def messageQuery(self):
        if self.__messageQuery == None:
            da = self.context.zsqlalchemy 
            assert da, 'No data-adaptor found'
            self.__messageQuery = \
              MessageQuery(self.context, da)
        assert self.__messageQuery
        return self.__messageQuery

    @property
    def topicId(self):
        if self.__topicId == None:
            self.__topicId = \
              self.messageQuery.topic_id_from_post_id(self.postId)
            if not self.__topicId:
                self.__topicId = \
                  self.topic_id_from_legacy_post_id(self.postId)
        assert self.__topicId != None
        return self.__topicId
        
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
        return self.topic[-1]['post_id']

    @property
    def topicName(self):
        if self.__topicName == None:
            self.__topicName = self.topic[0]['subject']
        assert self.__topicName != None
        return self.__topicName
    
    @property
    def nextTopic(self):
        if self.__nextTopic == None:
            r = self.messageQuery.later_topic(self.topicId)
            if r:
                self.__nextTopic = TopicInfo(r['last_post_id'], r['subject'])
            else:
                self.__nextTopic = TopicInfo(None,None)
        assert self.__nextTopic != None
        return self.__nextTopic
        
    @property
    def previousTopic(self):
        if self.__previousTopic == None:
            r = self.messageQuery.earlier_topic(self.topicId)
            if r:
                self.__previousTopic = TopicInfo(r['last_post_id'], r['subject'])
            else:
                self.__previousTopic = TopicInfo(None,None)
        assert self.__previousTopic
        return self.__previousTopic

    @property
    def topicSticky(self):
        retval = self.topicId in self.get_sticky_topics()
        assert type(retval) == bool
        return retval

    def get_sticky_topics(self):
        if self.__stickyTopics == None:
            stickyTopicsIds = self.groupInfo.get_property('sticky_topics', [])
            if type(stickyTopicsIds) != list:
                stickyTopicsIds = list(stickyTopicsIds)
            self.__stickyTopics = stickyTopicsIds
        assert self.__stickyTopics != None
        assert type(self.__stickyTopics) == list
        return self.__stickyTopics

    @property
    def userIsAdmin(self):
        return user_admin_of_group(self.userInfo, self.groupInfo)

class TopicInfo(object):
    def __init__(self, topicId, subject):
        self.topicId = topicId
        self.subject = subject

