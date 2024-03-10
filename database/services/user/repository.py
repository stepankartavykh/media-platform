from database import DBSession
from database.models import User
from sqlalchemy.exc import IntegrityError


class UserRepository:
    def __init__(self):
        self.model = User

    @staticmethod
    def add(user: User):
        DBSession.add(user)
        try:
            DBSession.commit()
        except IntegrityError:
            DBSession.rollback()
