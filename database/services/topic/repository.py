from database import Session
from database.models import Topic, UserTopic, User


class TopicRepository:
    def __init__(self):
        pass

    @staticmethod
    def add_topic(id_, pid, name, rank):
        session = Session()
        session.add(Topic(id=id_,
                          pid=pid,
                          name=name,
                          rank=rank))
        session.commit()

    @staticmethod
    def get_topics(user_id):
        session = Session()
        topics = session.query(Topic).join(UserTopic).join(User).filter(User.id == user_id)
        session.close()
        return topics
