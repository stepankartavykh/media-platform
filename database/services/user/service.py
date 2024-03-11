from database.models import User
from database.services.user.repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository

    def add_user(self, id_, username):
        user = User(id=id_,
                    username=username,
                    email_address=f'test{id_}@mail.ru')
        self.repository.add(user)

    def get_user(self, user_id):
        return self.repository.get_user(user_id)
