import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4
from tqdm.auto import tqdm
import os
import pinecone
from pinecone import GRPCIndex
import argparse

parser = argparse.ArgumentParser(description="My Python app")
parser.add_argument(dest="query", help="Game-specific question")

args = parser.parse_args()

embed_model = "text-embedding-ada-002"

# initialize connection to pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_REGION")
)

#index_name = 'rook'
index_name = pinecone.list_indexes()[0]

index = pinecone.GRPCIndex(index_name)


# query = "What attribute is the Golden Goose?"
# query = "Where can I get capture cards?"
# query = "How much HP does the Decoy Pillar card have?"
# query = "What is the most powerful card?"
query = args.query

res = openai.Embedding.create(
    input=[query],
    engine=embed_model
)

# retrieve from Pinecone
xq = res['data'][0]['embedding']

# get relevant contexts (including the questions)
res = index.query(xq, top_k=5, include_metadata=True)

# print(res)

# get list of retrieved text
contexts = [item['metadata']['text'] for item in res['matches']]

augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

# system message to 'prime' the model
# primer = f"""You are Q&A bot. A highly intelligent system that answers
# user questions based on the information provided by the user above
# each question. If the information can not be found in the information
# provided by the user you truthfully say "I don't know".
# """

primer = f"""You are a video game Q&A bot. A highly intelligent system that answers
user questions based on the information provided by the user above
each question. If the information can not be found in the information
provided by the user you truthfully say "I don't know".
"""

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": primer},
        {"role": "user", "content": augmented_query}
    ]
)

print(res['choices'][0]['message']['content'])