from database import Session
from database.models import Topic, UserTopic, User


class TopicRepository:
    def __init__(self):
        pass

    @staticmethod
    def add_topic(pid, name, rank: int = 1):
        session = Session()
        session.add(Topic(pid=pid,
                          name=name,
                          rank=rank))
        session.commit()

    @staticmethod
    def get_topics(user_id):
        session = Session()
        topics = session.query(Topic).join(UserTopic).join(User).filter(User.id == user_id)
        session.close()
        return topics

    @staticmethod
    def add_topic_to_user_config(user_id, topic_id):
        session = Session()

        session.add(UserTopic(user_id=user_id,
                              topic_id=topic_id))
        session.commit()
