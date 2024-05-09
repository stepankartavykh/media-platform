from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query

from DataApp.cache_system import CacheSystem
from api.get_news_dump import get_news_feed_everything
from pydantic import BaseModel

app = FastAPI(debug=True)


class Subject:
    def __init__(self, params):
        self.params = params

    def queries(self) -> list[str]:
        for param in self.params:
            print(param)
        return ['example']


def get_queries(subject: Subject = None, params: dict = None) -> list[str]:
    if not subject:
        return ['investments', 'economics', 'physics', 'microelectronics']


@app.get("/load-queries-cash")
async def main():
    # queries = get_queries()
    cache_system = CacheSystem()
    file_paths = [get_news_feed_everything(topic) for topic in ['investments', 'economics', 'physics',
                                                                'microelectronics']]
    for number, path in enumerate(file_paths):
        section = number % 16
        cache_system.load_cache(path, section)
    # result = read_item(123, 234)
    result = {'status': "ok"}
    return result


@app.get("/accept-notification")
def read_item(user_id: int, chat_id: int):
    print(f'user_id = {user_id} in chat with chat_id = {chat_id}')

    return {"item_id": user_id, "chat_id": chat_id}


@app.get('/test')
def get(point: int):
    print(f'requests with {point} is processed in /test endpoint')
    return {'status': 'ok'}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    print(type(item))
    return item.name


@app.get("/items-ann")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
