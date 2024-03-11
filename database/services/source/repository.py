from database import Session
from database.models import Source, User, UserSource


class SourceRepository:
    def __init__(self):
        self.model = Source

    @staticmethod
    def add(source: Source):
        session = Session()
        s = session.query(Source).filter(Source.id == source.id).first()
        if not s:
            session.add(source)
            session.commit()
        session.close()

    @staticmethod
    def get_sources_for_user(user_id):
        session = Session()
        user_sources = session.query(Source).join(UserSource).join(User).filter(User.id == user_id).all()
        return user_sources
