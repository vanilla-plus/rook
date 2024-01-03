import numpy as np
import openai
import faiss

indexFilePath = "something.index"
index = faiss.read_index(indexFilePath)


def Save():
    faiss.write_index(index, indexFilePath)


def ingest(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    embeddings = response["data"][0]["embedding"]
    return embeddings


while True:
    user_input = input("")
    embeddings = ingest(user_input)
    index.add(np.array([embeddings], dtype=np.float32))
    Save()
