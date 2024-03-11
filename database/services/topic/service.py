from database.services.topic.repository import TopicRepository


class TopicService:
    def __init__(self):
        self.repository = TopicRepository

    def add_topic(self, id_, pid, name, rank):
        self.repository().add_topic(id_, pid, name, rank)

    def get_topics_for_user(self, user_id):
        return self.repository().get_topics(user_id)
