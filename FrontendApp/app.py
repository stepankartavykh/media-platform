import asyncio
import json
import random
import threading
import time
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from FrontendApp.interface_data import DataPacketInterface, AddArticleInterface, UpdateArticleInterface
from api.get_news_dump import get_news_feed_everything
from DataApp.storage_schemas.storage import Article, engine
from sqlalchemy.orm import Session


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


class ContentEvent:
    pass


EVENT_UPDATE_STATE = False


def event_generator() -> None:
    global EVENT_UPDATE_STATE
    while True:
        time.sleep(random.randint(3, 6))
        EVENT_UPDATE_STATE = True


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    thread = threading.Thread(target=event_generator, args=())
    thread.start()
    yield
    print('Shutdown procedures...')
    thread.join(timeout=3.0)


app = FastAPI(debug=True, lifespan=lifespan)


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
    for data_article in data['articles'][:consider_amount]:
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
                                                url=data_article.get('url') + str(uuid.uuid4())))
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
        print('loaded!')
        session.commit()
    return content_packet


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global EVENT_UPDATE_STATE
    await connection_manager.connect(websocket)
    try:
        while True:
            if EVENT_UPDATE_STATE:
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
