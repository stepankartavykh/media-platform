import asyncio
import json
import random
from abc import abstractmethod, ABC
from itertools import chain

from AnalysisApp.model import Metric


class TableMetric:
    pass


class ModelElement:
    pass


class BiasElement(ModelElement):
    pass


class ModelType:
    """
    List of all possible ML models for analysis.
    """
    @abstractmethod
    def __init__(self, pretrained: bool):
        pass

    @abstractmethod
    async def compare(self, first_element: ModelElement, second_element: ModelElement) -> float:
        raise NotImplementedError("Redefine compare method for model" + self.__class__.__name__)

    @abstractmethod
    async def add_text(self, input_text) -> None:
        pass


class BiasModel(ModelType, ABC):
    async def compare(self, first_element: BiasElement, second_element: BiasElement) -> float:
        pass


class TextPacket:
    """
    Article structured in a certain way.
    """
    def get_text(self) -> str:
        pass


async def text_to_vector(input_text: str, type_model: ModelType) -> None:
    await asyncio.sleep(random.random())
    await type_model.add_text(input_text)


async def run_comparison(first_text: str, second_text: str, type_model: ModelType = None, step: int = None) -> Metric:
    await asyncio.sleep(random.random() * 10)
    # TODO simulation of working model
    value_from_model = random.random()
    return Metric(score_value=value_from_model, unique_metric_name=step)


async def run_comparison_for_texts_sets(first_set: list[TextPacket],
                                        second_set: list[TextPacket],
                                        model: ModelType) -> TableMetric:
    tasks = []
    for i in range(len(first_set)):
        for j in range(i + 1, len(second_set)):
            tasks.append(asyncio.create_task(run_comparison(first_set[i].get_text(), second_set[j].get_text(), model, (i + 1) * 1000 + j * 10)))
    await asyncio.gather(*tasks)
    return TableMetric()


async def main():
    with open('/home/skartavykh/MyProjects/media-bot/storage/text_dump/start-texts-packets.json', 'r') as f:
        data = json.load(f)
    tasks = []
    text_elements = data['text_elements']
    for i in range(len(text_elements)):
        for j in range(i + 1, len(text_elements)):
            print(i, j)
            tasks.append(asyncio.create_task(run_comparison(text_elements[i], text_elements[j])))
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    for task in chain(done, pending):
        r = await task
        print(r.unique_name, r.score_value)


if __name__ == '__main__':
    asyncio.run(main())
