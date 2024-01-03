import os
import uuid

import chromadb

# Initialize chromadb
client = chromadb.PersistentClient(path="chromadb")

# Create the embedding function
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

collection = client.get_or_create_collection(
    name="general", embedding_function=openai_ef
)

# Actions

while True:
    statement = input(
        "\nPlease input some knowledge for Rook's memory. They benefit the most from short, concise factual statements. \n\n"
    )

    collection.add(
        documents=[statement],
        metadatas=[{"source": "user"}],
        ids=[str(uuid.uuid4())],
    )

    print("Success!\n\n")
