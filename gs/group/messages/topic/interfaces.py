# coding=utf-8
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from zope.schema import Bool, TextLine, Field, ASCIILine
from Products.XWFMailingListManager.interfaces import IGSPostMessage

class ITopicPage(IViewletManager):
      '''A viewlet manager for the topic page'''

class ITopicSummary(IViewletManager):
      '''A viewlet manager for the topic summary'''

class ITopicAdmin(IViewletManager):
      '''A viewlet manager for the topic administration function'''

class ITopicJavaScript(IViewletManager):
      '''A viewlet manager for the JavaScript on the topic page'''

class IGSAddToTopicFields(IGSPostMessage):
    u'''Fields used on the topic page.'''
    inReplyTo = TextLine(title=u'In Reply To Identifier',
      description=u'The ID of the most recent post to the topic',
      required=True)

