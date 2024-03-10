from database.models import User
from database.services.user.repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository

    def add_user(self, id_, username):
        user = User(id=id_,
                    username=username)
        self.repository.add(user)
