# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet

# TODO: Move to gs.group.member.canpost

class CannotAddToTopic(GroupViewlet):
    def __init__(self, messages, request, view, manager):
        GroupViewlet.__init__(self, messages, request, view, manager)

    @Lazy
    def show(self):
        postingInfo = self.view.userPostingInfo
        assert postingInfo
        retval = not(postingInfo.canPost)
        return retval

    @Lazy
    def statusNum(self):
        retval = self.view.userPostingInfo.statusNum
        return retval
        
    @Lazy
    def status(self):
        retval = self.view.userPostingInfo.status
        return retval

