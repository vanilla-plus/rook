import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest="relative_filepath", help="Game-related question")

args = parser.parse_args()

# from langchain.document_loaders import ReadTheDocsLoader
from langchain.document_loaders import TextLoader

# from langchain.document_loaders import DirectoryLoader

# relative_filepath = 'rtdocs/Lost Kingdoms II/23736.txt'
relative_filepath = args.relative_filepath

loader = TextLoader(relative_filepath, encoding="utf8")
docs = loader.load()
len(docs)

text = docs[0].page_content

import tiktoken

tokenizer = tiktoken.get_encoding("p50k_base")


# create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""],
)

texts = text_splitter.split_text(text)

from uuid import uuid4
from tqdm.auto import tqdm

chunks = []

for idx, record in enumerate(tqdm(docs)):
    texts = text_splitter.split_text(record.page_content)
    chunks.extend(
        [
            {"id": str(uuid4()), "text": texts[i], "chunk": i, "url": ""}
            for i in range(len(texts))
        ]
    )

import openai

embed_model = "text-embedding-ada-002"

res = openai.Embedding.create(input=texts, engine=embed_model)

# res.keys()

# print(res)

# with open("embedding.txt", "w") as file:
#     file.write(res.keys())

import os
import pinecone
from pinecone import GRPCIndex


# initialize connection to pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_REGION")
)

# index_name = 'rook'
# index_name = 'gcn-lost-kingdoms-ii'

index_name = pinecone.list_indexes()[0]

# connect to index
index = pinecone.GRPCIndex(index_name)

index.describe_index_stats()

from tqdm.auto import tqdm
import datetime
from time import sleep

batch_size = 100  # how many embeddings we create and insert at once

for i in tqdm(range(0, len(chunks), batch_size)):
    # find end of batch
    i_end = min(len(chunks), i + batch_size)
    meta_batch = chunks[i:i_end]
    # get ids
    ids_batch = [x["id"] for x in meta_batch]
    # get texts to encode
    texts = [x["text"] for x in meta_batch]
    # create embeddings (try-except added to avoid RateLimitError)
    try:
        res = openai.Embedding.create(input=texts, engine=embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(input=texts, engine=embed_model)
                done = True
            except:
                pass
    embeds = [record["embedding"] for record in res["data"]]
    # cleanup metadata
    meta_batch = [
        {"text": x["text"], "chunk": x["chunk"], "url": x["url"]} for x in meta_batch
    ]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))

    # print(ids_batch)
    # print(embeds)
    # print(meta_batch)

    # print(to_upsert)

    # upsert to Pinecone
    index.upsert(vectors=to_upsert)
