from database import DBSession, Session
from database.models import User
from sqlalchemy.exc import IntegrityError


class UserRepository:
    def __init__(self):
        self.model = User

    @staticmethod
    def add(user: User):
        session = Session()
        u = session.query(User).filter(User.id == user.id).first()
        if not u:
            session.add(user)
            session.commit()
        session.close()

    @staticmethod
    def get_user(id_):
        session = Session()
        user = session.query(User).filter(User.id == id_)
        session.close()
        return user
