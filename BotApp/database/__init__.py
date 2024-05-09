from BotApp.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DATABASE_NAME, POSTGRES_PORT
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, DeclarativeBase, sessionmaker


def get_engine_url() -> str:
    asyncpg_driver = '+asyncpg'
    default_driver = ''
    return '{dialect}{driver}://{username}:{password}@{host}:{port}/{database}'.format(
        dialect='postgresql',
        driver=default_driver,
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE_NAME,
    )


class SessionFactory(Session):

    def __init__(self) -> None:
        super().__init__(autoflush=False)
        self.url = self._url
        self.bind = self._engine

    @property
    def _url(self) -> str:
        asyncpg_driver = '+asyncpg'
        default_driver = ''
        return '{dialect}{driver}://{username}:{password}@{host}:{port}/{database}'.format(
            dialect='postgresql',
            driver=default_driver,
            username=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DATABASE_NAME,
        )

    @property
    def _engine(self) -> Engine:
        return create_engine(self.url, echo=True)


engine_ = create_engine(get_engine_url())
Session = sessionmaker(engine_)


class Base(DeclarativeBase):
    pass


DBSession = scoped_session(SessionFactory)
