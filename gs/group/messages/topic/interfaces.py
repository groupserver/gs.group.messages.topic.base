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

class IGSStickyTopicToggleContentProvider(Interface):
    """A content provider for the sticky-topic toggle"""
    topic = TextLine(title=u"Topic",
        description=u"The name of the topic to be toggled",
        required=True)
    topicId = ASCIILine(title=u"Topic ID",
        description=u"The ID of the topic to be toggled",
        required=True)
    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u"""The name of the ZPT file
        that is used to render the form.""",
        required=False,
        default="browser/templates/stickytoggle.pt")

