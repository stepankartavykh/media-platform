import asyncio
import json
import os
import random
import threading
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from DataApp.cache_system import CacheSystem
from FrontendApp.interface_data import DataPacketInterface, AddArticleInterface, UpdateArticleInterface
from api.get_news_dump import get_news_feed_everything
from DataApp.storage_schemas.storage import Article, engine
from sqlalchemy.orm import Session
from aiohttp import ClientSession

from dotenv import load_dotenv

load_dotenv()


def define_topic_for_api_call() -> str:
    possible_topics = ["economics", "microelectronics", "quantum computing", "investing", "research technologies",
                       "medicine", "water desalination", "physics", "economics reports", "microchips new research",
                       "power", "new sources energy"]
    if not possible_topics:
        possible_topics.append("news")
    return random.choice(possible_topics)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data_package: str):
        broadcast_tasks = [connection.send_text(data_package)
                           for connection in self.active_connections]
        await asyncio.gather(*broadcast_tasks)


connection_manager = ConnectionManager()
cache_system_plugin = CacheSystem()


class ContentEvent:
    pass


EVENT_UPDATE_STATE = False


def event_generator() -> None:
    global EVENT_UPDATE_STATE
    while True:
        time.sleep(random.randint(10, 20))
        EVENT_UPDATE_STATE = True


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    if not os.getenv('IS_CACHE_SERVICE_UPDATE_READY'):
        cache_system_plugin.load_initial_data()
    thread = threading.Thread(target=event_generator, args=())
    thread.start()
    yield
    print('Shutdown procedures...')
    thread.join(timeout=1.0)


app = FastAPI(debug=True, lifespan=lifespan)


async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


async def generate_article_content(from_api: bool = True, consider_amount: int | None = None) -> DataPacketInterface:
    if not from_api:
        raise NotImplementedError('Implementation of dump load is required!')
    extracted_data_path = get_news_feed_everything(topic=define_topic_for_api_call())
    with open(extracted_data_path, 'r') as f:
        data = json.load(f)
    articles_to_add = []
    articles_to_update = []
    articles_to_database = []
    if not consider_amount:
        consider_amount = len(data['articles'])
    with Session(engine) as session:
        all_articles_urls = session.query(Article.url).all()
    all_articles_urls = set(all_articles_urls)
    all_urls = [art.get('url') for art in data['articles'][:consider_amount]]
    filtered_urls = set()
    async with ClientSession() as session:
        tasks = []
        for url in all_urls:
            tasks.append(fetch_status(session, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                # TODO custom exception (must be processed in layer above)
                print("EXCEPTION (BAD URL):", all_urls[i])
            else:
                print('GOOD URL (FOR NEXT SEARCH ITERATION):', all_urls[i])
                filtered_urls.add(all_urls[i])
    for data_article in data['articles'][:consider_amount]:
        if data_article.get('url') in all_articles_urls:
            print('Same article!')
            continue
        if data_article.get('url') not in filtered_urls:
            continue
        if random.randint(1, 10) < 6:
            add_article = AddArticleInterface(source=data_article.get('source', {'name': "Unknown"}).get('name'),
                                              priority=random.randint(1, 10),
                                              author=data_article.get('author', 'Unknown'),
                                              title=data_article.get('title', 'Unknown'),
                                              description=data_article.get('description', 'None'),
                                              url=data_article.get('url'),
                                              urlToImage=data_article.get('urlToImage'),
                                              publishedAt=data_article.get('publishedAt'),
                                              content=data_article.get('content'))
            articles_to_database.append(Article(author=data_article.get('author', 'Unknown'),
                                                title=data_article.get('title', 'Unknown'),
                                                description=data_article.get('description', 'None'),
                                                content=data_article.get('content'),
                                                published_at=data_article.get('publishedAt'),
                                                url=data_article.get('url')))
            articles_to_add.append(add_article)
        else:
            update_article = UpdateArticleInterface(update_type=random.choice(('update', 'add_content', 'replace')),
                                                    priority=random.randint(1, 10),
                                                    source=data_article.get('source', {'name': "Unknown"}).get('name'),
                                                    author=data_article.get('author', 'Unknown'),
                                                    title=data_article.get('title', 'Unknown'),
                                                    description=data_article.get('description', 'None'),
                                                    url=data_article.get('url'),
                                                    urlToImage=data_article.get('urlToImage'),
                                                    publishedAt=data_article.get('publishedAt'),
                                                    content=data_article.get('content'))
            articles_to_update.append(update_article)
    content_packet = DataPacketInterface(articlesAdd=articles_to_add,
                                         articlesUpdate=articles_to_update)
    with open(f'/home/skartavykh/MyProjects/media-bot/storage/data_packets/{time.time_ns()}.json', 'w') as f:
        json.dump(jsonable_encoder(content_packet), f)
    with Session(engine) as session:
        session.add_all(articles_to_database)
        session.commit()
    return content_packet


class ActualContent:
    def __init__(self, data):
        self.data = data


async def get_current_content(get_from_cache_directly: bool = False) -> ActualContent:
    content = None
    if get_from_cache_directly:
        content = await cache_system_plugin.get_actual_content()
    return ActualContent(data=content)


@app.get("/change-frontend-state-signal")
async def accept_signal_to_change_frontend_state():
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global EVENT_UPDATE_STATE
    await connection_manager.connect(websocket)
    try:
        while True:
            if EVENT_UPDATE_STATE:
                actual_content = await get_current_content()
                data_packet = await generate_article_content()
                await connection_manager.broadcast(data_packet.json())
                print('broadcasting current state is complete!')
                EVENT_UPDATE_STATE = False
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f'websocket {websocket.client_state.value} closed!')


def run_app():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    run_app()
