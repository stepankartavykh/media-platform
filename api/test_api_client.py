from newsapi import NewsApiClient
from api.config import NEWS_API_KEY

newsapi_client = NewsApiClient(api_key=NEWS_API_KEY)

top_headlines = newsapi_client.get_top_headlines(q='bitcoin',
                                                 category='business',
                                                 language='en',
                                                 country='us')
print(top_headlines)
# all_articles = newsapi_client.get_everything(q='bitcoin',
#                                              sources='bbc-news,the-verge',
#                                              domains='bbc.co.uk,techcrunch.com',
#                                              from_param='2017-12-01',
#                                              to='2017-12-12',
#                                              language='en',
#                                              sort_by='relevancy',
#                                              page=2)
#
# sources = newsapi_client.get_sources()
