from database.services.topic.repository import TopicRepository


class TopicService:
    def __init__(self):
        self.repository = TopicRepository

    def add_topic(self, pid, name, rank):
        self.repository().add_topic(pid, name, rank)

    def get_topics_for_user(self, user_id):
        return self.repository().get_topics(user_id)

    def add_topic_for_user_preference(self, user_id: int, topic_id: int):
        self.repository.add_topic_to_user_config(user_id, topic_id)
