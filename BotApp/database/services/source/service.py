from database.models import Source
from database.services.source.repository import SourceRepository


class SourceService:
    def __init__(self):
        self.repository = SourceRepository

    def get_source_by_url(self, url):
        s = self.repository.get_source(url)
        if s:
            return s.id
        return None

    def add_source(self, url, id_=None, source_name='Unknown source name'):
        """
        Adding source to database.
        @param id_: identifier of source TODO - maybe delete
        @param url: url of main page of the source (UNIQUE CONSTRAINT)
        @param source_name: name of the source (e.g. "DailyNews")
        """
        s = Source(id=id_,
                   url=url,
                   name=source_name)
        self.repository.add(s)

    def add_source_for_user(self, user_id, source_id):
        self.repository.add_source_for_user(user_id, source_id)

    def get_sources_for_user(self, user_id):
        self.repository.get_sources_for_user(user_id)
