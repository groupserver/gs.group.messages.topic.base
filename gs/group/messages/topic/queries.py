# coding=utf-8
import sqlalchemy as sa
from datetime import datetime
from zope.sqlalchemy import mark_changed
from gs.database import getSession, getTable


class TopicQuery(object):
    def __init__(self, context):
        self.context = context

        self.topicTable = getTable('topic')
        self.postTable = getTable('post')

    def topic_hidden(self, postId):
        s1 = sa.select([self.postTable.c.topic_id])
        s1.append_whereclause(self.postTable.c.post_id == postId)
        s1.alias('ss')

        s2 = sa.select(self.topicTable.hidden)
        s2.append_whereclause(ss.c.topic_id)  # lint:ok

        session = getSession()
        r = session.execute(s2)
        x = r.fetchone()
        retval = bool(x['hidden'])
        return retval

    def topic_sticky(self, topicId):
        s = sa.select([self.topicTable.c.sticky])
        s.append_whereclause(self.topicTable.c.topic_id == topicId)
        session = getSession()
        r = session.execute(s)

        x = r.fetchone()
        retval = bool(x['sticky'])
        return retval

    def set_sticky(self, topicId, sticky):
        session = getSession()
        tt = self.topicTable
        u = tt.update(tt.c.topic_id == topicId)
        if sticky:
            v = datetime.utcnow()
        else:
            v = None
        d = {'sticky': v}
        session.execute(u, params=d)
        mark_changed(session)
