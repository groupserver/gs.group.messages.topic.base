# coding=utf-8
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from zope.schema import ASCIILine, Bool, Bytes, Choice, Field, Text, TextLine

class ITopicPage(IViewletManager):
      '''A viewlet manager for the topic page'''

class ITopicSummary(IViewletManager):
      '''A viewlet manager for the topic summary'''

class ITopicAdmin(IViewletManager):
      '''A viewlet manager for the topic administration function'''

class ITopicJavaScript(IViewletManager):
      '''A viewlet manager for the JavaScript on the topic page'''

class IGSPostMessage(Interface):
    fromAddress = Choice(title=u'Email From',
      description=u'The email address that you want in the "From" '\
        u'line in the email you send.',
      vocabulary = 'EmailAddressesForLoggedInUser',
      required=True)

    message = Text(title=u'Message',
      description=u'The message you want to post to this topic.',
      required=True)
    
    uploadedFile = Bytes(title=u'Files',
                         description=u'A file you wish to add.',
                         required=False)


class IGSAddToTopicFields(IGSPostMessage):
    u'''Fields used on the topic page.'''
    inReplyTo = TextLine(title=u'In Reply To Identifier',
      description=u'The ID of the most recent post to the topic',
      required=True)

