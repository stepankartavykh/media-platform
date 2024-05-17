import json
import random
import time

from api.get_news_dump import get_news_feed_everything
from api.interfaces.news_sources import EverythingResponseInterface


def define_topic_for_api_call() -> str:
    possible_topics = ["economics", "microelectronics", "quantum computing"]
    if not possible_topics:
        possible_topics.append("news")
    return random.choice(possible_topics)


def data_pipeline_simulation():
    for i in range(3):
        topic = define_topic_for_api_call()
        dump_path = get_news_feed_everything(topic)
        with open(dump_path, 'r') as f:
            data = json.load(f)
        everything_on_topic = EverythingResponseInterface.model_validate(data)
        for article in everything_on_topic.articles[:15]:
            print(article.published_at)
        time.sleep(3)


if __name__ == '__main__':
    main()
