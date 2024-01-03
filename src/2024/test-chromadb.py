import os
import uuid
import chromadb

# Create the client

# chroma_client = chromadb.Client()
client = chromadb.PersistentClient(path="db")

# Create the embedding function
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

# Create or open the collection

# collection = client.get_or_create_collection(name="default-embeddings")

collection = client.get_or_create_collection(
    name="openai-embeddings", embedding_function=openai_ef
)

some_text = input("Say something: ")

# collection.add(
#     documents=["This is the hook.", "You like it."],
#     metadatas=[{"source": "debug"}, {"source": "debug"}],
#     ids=["id1", "id2"],
# )

collection.add(
    documents=[some_text],
    metadatas=[{"source": "debug"}],
    ids=[str(uuid.uuid4())],
)

results = collection.query(query_texts=["This is the hook?"], n_results=2)

# for result in results:
# print("HERE I GO")
# print(result)

print(results)

# Lowest distance wins!
