# coding=utf-8
from zope.cachedescriptors.property import Lazy
from gs.group.base.viewlet import GroupViewlet

# TODO: Move to gs.group.member.canpost

class CannotAddToTopic(GroupViewlet):
    '''The suppplier of *ahem* the can-post viewlet manager'''

