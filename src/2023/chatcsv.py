import os
import openai

import pandas as pd

from openai.embeddings_utils import cosine_similarity


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

memFilePath = "memory.csv"

try:
    with open(memFilePath, "x") as f:
        f.write("text,embedding\n")
except FileExistsError:
    pass

# df["embedding"] = df["text"].apply(
#     lambda x: get_embedding(x, engine="text-embedding-ada-002")
# )

# df.to_csv(memFilePath)

while True:
    print("User:")
    newText = input("")
    embeddingRequest = openai.Embedding.create(
        input=[newText], engine="text-embedding-ada-002"
    )
    newEmbedding = embeddingRequest["data"][0]["embedding"]
    # newEntry = pd.DataFrame([newEmbedding], [newText])

    # df.add(newEntry)

    # Create a new DataFrame with the user input and embedding, and append it to the CSV file
    df = pd.DataFrame(data=[[newText, newEmbedding]], columns=["text", "embedding"])

    df["similarities"] = df["embedding"].apply(lambda x: cosine_similarity(x, newText))

    df.to_csv(memFilePath, mode="a", header=False, index=False)
