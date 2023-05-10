import os
import argparse
import openai
import numpy as np
import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

# Initialize argparse
parser = argparse.ArgumentParser()

parser.add_argument(dest="indexFilePath", help="relative .index filePath")

args = parser.parse_args()

# Initialize faiss index
indexFileName = args.indexFilePath

indexFilePath = indexFileName + ".index"
if os.path.exists(indexFilePath):
    index = faiss.read_index(indexFilePath)
else:
    d = 1536  # Exact dimensionality of text-embedding-ada-002 vectors
    index = faiss.IndexFlatL2(d)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize Faiss index
# index = faiss.IndexFlatL2(1536)

# Set up tokenizer
tokenizer = tiktoken.get_encoding("p50k_base")


def tiktoken_len(text):
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


# Set up text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""],
)

# Embedding function
embed_model = "text-embedding-ada-002"


def create_embedding(text):
    res = openai.Embedding.create(input=[text], engine=embed_model)
    return res["data"][0]["embedding"]


conversation = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant capable of discussing a wide range of topics. As the conversation progresses, you may receive potentially relevant context to help you understand the user's questions and provide better assistance. Use this context to enhance your responses and offer accurate information.",
    }
]


# def AddTextToIndex(text):
#     embedding = create_embedding(text)
#     index.add(np.array([embedding], dtype=np.float32))


def AddTextToIndex(text):
    embedding = create_embedding(text)
    print("Adding embedding:", embedding)
    index.add(np.array([embedding], dtype=np.float32))
    print("Index size:", index.ntotal)


def WriteIndexToLocalStorage():
    faiss.write_index(index, indexFilePath)


def UserTurn():
    print("\nUser:")

    user_input = input("")

    conversation.append({"role": "user", "content": user_input})

    # Add user_input to the vector database
    AddTextToIndex(user_input)

    WriteIndexToLocalStorage()


def AITurn():
    # Perform a similarity search in the index
    n_results = 5
    last_message = conversation[-1]["content"]
    last_embedding = create_embedding(last_message)
    _, indices = index.search(np.array([last_embedding], dtype=np.float32), n_results)

    # print("Indices:", indices)  # Add this line

    # Retrieve the texts associated with the most similar embeddings
    # similar_texts = [conversation[idx]["content"] for idx in indices[0] if idx != -1]

    print("Indices:", indices)
    print("Indices shape:", indices.shape)
    print("Conversation:", conversation)

    # similar_texts = [
    #     conversation[idx]["content"]
    #     for idx in indices[0]
    #     if idx != -1 and idx < len(conversation)
    # ]

    print("Indices to be used:", [idx for idx in indices[0] if idx != -1])
    similar_texts = [conversation[idx]["content"] for idx in indices[0] if idx != -1]
    print("Similar texts:", similar_texts)

    for t in similar_texts:
        print("Snerp")
        print(t)

    # print("Similar texts:", similar_texts)  # Add this line

    # Combine the conversation with the retrieved similar_texts
    augmented_conversation = conversation + [
        {"role": "user", "content": text} for text in similar_texts
    ]

    # for text in augmented_conversation:
    #  print(text)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=augmented_conversation,
        temperature=0.7,
        max_tokens=250,
        top_p=0.9,
    )

    reply = response["choices"][0]["message"]["content"]

    conversation.append({"role": "assistant", "content": reply})

    print("\nAssistant:\n" + reply)

    AddTextToIndex(reply)

    WriteIndexToLocalStorage()


# Back and forth forever
while True:
    UserTurn()
    AITurn()
