from bertopic import BERTopic


import json


topic_model = BERTopic(embedding_model="all-MiniLM-L6-v2")


def prepare_data(docs: list[dict]) -> list[str]:
    data_ = []
    for doc in docs:
        if doc.get('description'):
            data_.append(doc.get('description'))
    return data_


def get_topics_and_props(entries_to_process: list[str]):
    topics, probs = topic_model.fit_transform(entries_to_process)
    return topics, probs


def get_data_from_file(file_path):
    with open(file_path) as f:
        docs = json.load(f)
    return docs


if __name__ == '__main__':
    data = get_data_from_file('/home/skartavykh/MyProjects/media-bot/storage/ukraine.json')
