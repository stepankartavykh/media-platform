class User:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name


class Source:
    def __init__(self, user_id, source_url):
        self.user_id = user_id
        self.url = source_url


class Topic:
    def __init__(self, user_id, value):
        self.user_id = user_id
        self.value = value
