# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")

import json
import time

import numpy as np
import pandas as pd
import redis
import requests
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer


from sentence_transformers import SentenceTransformer
import redis
from redisai import Client

# Load the sentence transformer model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Initialize Redis connection
redis_host = 'localhost'
redis_port = 6378
redis_db = 0
redis_password = None

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
redisai_client = Client()

sentences = [
    "This is the first sentence.",
    "Another sentence goes here.",
    "One more example sentence."
]


def main():
    embeddings = model.encode(sentences)

    for i, embedding in enumerate(embeddings):
        key = f"embedding:{i+1}"
        redisai_client.tensorset(key, embedding.tolist())

    print("Embeddings loaded into Redis vector database!")


if __name__ == '__main__':
    main()
