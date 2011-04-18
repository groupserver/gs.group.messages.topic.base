# coding=utf-8
from operator import and_
import sqlalchemy as sa
from datetime import datetime
from pytz import UTC

class TopicQuery(object):
    def __init__(self, context, da):
        self.context = context
        
        self.topicTable = da.createTable('topic')
        self.postTable = da.createTable('post')

    def topic_hidden(self, postId):
        s1 = sa.select([self.postTable.c.topic_id])
        s1.append_whereclause(self.postTable.c.post_id == postId)
        s1.salias('ss')

        s2 = sa.select(self.topicTable.hidden)
        s2.append_whereclause(ss.c.topic_id)
        
        r = s2.execute()
        x = r.fetchone()
        retval = bool(x['hidden'])
        return retval

