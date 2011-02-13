# coding=utf-8
from zope.interface import Interface
from zope.schema import Bool, TextLine 
from Products.XWFMailingListManager.interfaces import IGSPostMessage

class IGSStickyTopic(Interface):
    sticky = Bool(title=u'Sticky',
      description=u'Display this topic before all other topics on '\
        u'the Latest Topics page.',
      required=False)

class IGSAddToTopicFields(IGSPostMessage, IGSStickyTopic):
    u'''Fields used on the topic page.'''
    inReplyTo = TextLine(title=u'In Reply To Identifier',
      description=u'The ID of the most recent post to the topic',
      required=True)

