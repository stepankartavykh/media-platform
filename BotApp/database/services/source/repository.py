from typing import Type

from database import Session
from database.models import Source, User, UserSource


class SourceRepository:
    def __init__(self):
        self.model = Source

    @staticmethod
    def add(source: Source):
        url = source.url
        session = Session()
        all_sources = session.query(Source).filter(Source.url == source.url).all()
        if all_sources:
            session.close()
            return all_sources[0].id
        session.add(source)
        session.commit()
        session.close()
        return session.query(Source).filter(Source.url == url).one().id

    @staticmethod
    def get_sources_for_user(user_id: int) -> list[Type[Source]]:
        session = Session()
        user_sources = session.query(Source).join(UserSource).join(User).filter(User.id == user_id).all()
        session.close()
        return user_sources

    @staticmethod
    def add_source_for_user(user_id, source_id) -> None:
        """
        @param self:
        @param user_id:
        @param source_id:
        """
        user_source = UserSource(user_id=user_id,
                                 source_id=source_id)
        session = Session()
        session.add(user_source)
        session.commit()
        session.close()

    @staticmethod
    def get_source(url: str) -> Type[Source]:
        # if url.startswith('https://')
        session = Session()
        source = session.query(Source).filter(Source.url == url).all()
        if len(source):
            source = source[0]
        session.close()
        return source


if __name__ == '__main__':
    test = Source(url='https://www.washingtonpost.com/qwe')
    print(SourceRepository.add(test))
