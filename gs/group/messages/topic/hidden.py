# coding=utf-8
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFFileLibrary2.hidden import FileHidden

class TopicHidden(FileHidden):
    index = ZopeTwoPageTemplateFile('browser/templates/topic.pt')
    def __init__(self, context, request):
        request.form['q'] = request.URL
        request.form['f'] = request['postId']
        FileHidden.__init__(self, context, request)
    
