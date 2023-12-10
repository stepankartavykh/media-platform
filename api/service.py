def form_request(api_url, params):
    pass


class CommonService:
    def __init__(self, url, params):
        self.api_url = url
        self.params = params
        self.url = self._url

    @property
    def _url(self):
        return ''

    async def make_query(self):
        pass