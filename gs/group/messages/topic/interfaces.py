# coding=utf-8
from zope.interface import Interface
from zope.schema import Bool, TextLine, Field, ASCIILine
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


class INavLinksContentProvider(Interface):
    topicTitle = TextLine(title=u"Title of the Topic",
        description=u'The title of the topic.',
        required=True)
                     
    previousTopic = Field(title=u'Previous Topic',
        description=u'The previous topic in the group same topic.',
        required=True)

    nextTopic = Field(title=u'Next Topic',
        description=u'The next topic in the group same topic.',
        required=True)

    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u"""The name of the ZPT file
        that is used to render the post.""",
        required=False,
        default='browser/templates/navlinks.pt')
                              
class IGSFileIndexContentProvider(Interface):
    """The Groupserver File Index Content Provider Interface
      
      This interface defines the fields that must be set up, normally using
      TAL, before creating a "GSTopicSummaryContentProvider" instance. 
      See the latter for an example."""
    
    topic = Field(title=u"Topic",
        description=u"The topic to display",
        required=True, 
        readonly=False)

    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u"""The name of the ZPT file
        that is used to render the post.""",
        required=False,
        default="browser/templates/fileindex.pt")

