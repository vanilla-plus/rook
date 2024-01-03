import os

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
    id = input("\nPlease input an index to remove from Rook's persistent memory. \n\n")

    collection.delete(ids=[id])

    print("Success!\n\n")
