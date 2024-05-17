import asyncio
from random import random
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query, Body

from AnalysisApp.ml_models.bias import load_bias_model
from DataApp.cache_system import CacheSystem
from api.get_news_dump import get_news_feed_everything
from pydantic import BaseModel


async def clustering_model(x: float) -> float:
    await asyncio.sleep(random() * 3)
    return x * random()


async def bias_model(x: float) -> float:
    await asyncio.sleep(random() * 3)
    return x * random()


async def first_test_model(x: float) -> float:
    await asyncio.sleep(random() * 3)
    return x * 4


async def second_test_model(x: float) -> float:
    await asyncio.sleep(random() * 3)
    return x * 4


possible_text_models = {}


def load_start_cache_logic() -> None:
    print("START: cache is loading...")
    print("FINISHED: cache is ready...")
    pass


@asynccontextmanager
async def lifespan(app_: FastAPI):
    load_start_cache_logic()
    possible_text_models["bias_model"] = load_bias_model
    possible_text_models["first_test_model"] = first_test_model
    possible_text_models["second_test_model"] = second_test_model
    possible_text_models[""] = bias_model
    yield
    possible_text_models.clear()


app = FastAPI(debug=True, lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = await possible_text_models["bias_model"](x)
    return {"result": result}


class TextPair(BaseModel):
    first_text: str
    second_text: str
    type_model: str


@app.post("/compare_texts")
async def run_comparison_view(text_pair: TextPair = Body(...)):
    await asyncio.sleep(2)
    print("first:", text_pair.first_text[:20])
    print("second:", text_pair.second_text[:20])
    print("type_model:", text_pair.type_model)
    return {"result": "two text packets are processed!", "status": 200}


@app.post("/send_text")
async def send_text(text: str = Body(...)):
    await asyncio.sleep(1)
    print("test snippet:", text[:10])
    return {"message": "Text received successfully"}


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
