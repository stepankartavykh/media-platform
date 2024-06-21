import asyncio
import json
import random
import threading
import time
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from DataApp.dataflow.main import define_topic_for_api_call
from FrontendApp.interface_data import DataPacketInterface, AddArticleInterface, UpdateArticleInterface
from api.get_news_dump import get_news_feed_everything


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


event_update_state = False


def event_generator() -> None:
    global event_update_state
    while True:
        print('DEBUG: event generator')
        time.sleep(random.randint(10, 20))
        event_update_state = True


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    thread = threading.Thread(target=event_generator, args=())
    thread.start()
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan)


def generate_article_content(from_api: bool = True) -> DataPacketInterface:
    if not from_api:
        raise NotImplementedError('Implementation of dump load is required!')
    extracted_data_path = get_news_feed_everything(define_topic_for_api_call())
    with open(extracted_data_path, 'r') as f:
        data = json.load(f)
    articles_to_add = []
    articles_to_update = []
    for data_article in data['articles'][:50]:
        if random.randint(1, 10) < 6:
            add_article = AddArticleInterface(
                source=data_article.get('source', {'name': "Unknown"}).get('name'),
                priority=random.randint(1, 10),
                author=data_article.get('author', 'Unknown'),
                title=data_article.get('title', 'Unknown'),
                description=data_article.get('description', 'None'),
                url=data_article.get('url'),
                urlToImage=data_article.get('urlToImage'),
                publishedAt=data_article.get('publishedAt'),
                content=data_article.get('content'),
            )
            articles_to_add.append(add_article)
        else:
            update_article = UpdateArticleInterface(
                update_type=random.choice(('update', 'add_content', 'replace')),
                priority=random.randint(1, 10),
                source=data_article.get('source', {'name': "Unknown"}).get('name'),
                author=data_article.get('author', 'Unknown'),
                title=data_article.get('title', 'Unknown'),
                description=data_article.get('description', 'None'),
                url=data_article.get('url'),
                urlToImage=data_article.get('urlToImage'),
                publishedAt=data_article.get('publishedAt'),
                content=data_article.get('content'),
            )
            articles_to_update.append(update_article)
    content_packet = DataPacketInterface(articlesAdd=articles_to_add,
                                         articlesUpdate=articles_to_update)
    return content_packet


def trigger_update_frontend_content():
    print('updates were send to users')
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            if event_update_state:
                await connection_manager.broadcast(generate_article_content().json())
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f'websocket {websocket.client_state.value} closed!')


def run_app():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    run_app()
