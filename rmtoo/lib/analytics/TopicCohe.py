'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Coherence of one topic.

 (c) 2010-2011 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.analytics.Base import Base
from rmtoo.lib.analytics.Result import Result

class TopicCohe(Base):
    '''Class for checking topic coherence.'''

    def __init__(self, config):
        '''Sets up the TopicCohe object for use.'''
        Base.__init__(self)
        self.__req2topics = {}
        self.__tcnt = {}

    def __add_req2topic(self, req_id, topic):
        '''Add req_id / topic to cache.'''
        if req_id not in self.__req2topics:
            self.__req2topics[req_id] = []
        self.__req2topics[req_id].append(topic)

    def topic_pre(self, topic):
        '''Collect the relation between requirement and topic.'''
        req_set = topic.get_requirement_set()
        if None == req_set:
            return
        for req_id in req_set.get_all_requirement_ids():
            self.__add_req2topic(req_id, topic)

    def __add_topic_relation(self, topic_a, topic_b):
        '''Add the relation between topic_a and topic_b.'''
        # If not there, add the initial count [0, 0]
        for topic in [topic_a.name, topic_b.name]:
            if not topic in self.__tcnt:
                self.__tcnt[topic] = [0, 0]

        # Add relation to both directions if the topic is the same or
        # a parent of the topic.

        # Iff self: add a 3!
        if topic_a == topic_b:
            self.__tcnt[topic_a.name][0] += 3
        elif topic_a.is_self_of_ancient(topic_b):
            # 2: because it is one incoming and one outgoing
            self.__tcnt[topic_b.name][0] += 2
        else:
            self.__tcnt[topic_a.name][1] += 1
            self.__tcnt[topic_b.name][1] += 1

    def __eval_link(self, req_a, req_b):
        '''Add all the links between all topics of req_a and req_b.'''
        for topic_a in self.__req2topics[req_a.get_id()]:
            for topic_b in self.__req2topics[req_b.get_id()]:
                self.__add_topic_relation(topic_a, topic_b)

    def topics_set_post(self, topic_set):
        '''This is call in the TopicsSet post-phase.'''
        for req_id in self.__req2topics.keys():
            req_a = topic_set.get_topic_set().get_requirement_set().\
                       get_requirement(req_id)
            for req_b in req_a.incoming:
                self.__eval_link(req_a, req_b)

        for topic, cnt in self.__tcnt.iteritems():
            if cnt[0] <= cnt[1]:
                self.add_result(Result("TopicCohe", topic,
                                - 10, ["%s: Topic coherence inadequate: "
                                       "inner %d / outer %d"
                                       % (topic, cnt[0], cnt[1])]))
