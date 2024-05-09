from typing import Type

from database import DBSession, Session
from database.models import User, UserSource
from sqlalchemy.exc import IntegrityError


class UserRepository:
    def __init__(self):
        self.model = User

    @staticmethod
    def add(user: User) -> None:
        session = Session()
        u = session.query(User).filter(User.id == user.id).first()
        if not u:
            session.add(user)
            session.commit()
        session.close()

    @staticmethod
    def get_user(id_) -> Type[User]:
        session = Session()
        user = session.query(User).filter(User.id == id_).one()
        session.close()
        return user

    @classmethod
    def add_source_for_user(cls, user_id, source_id) -> None:
        session = Session()
        session.add(UserSource(user_id=user_id,
                               source_id=source_id))
        session.commit()
        session.close()
