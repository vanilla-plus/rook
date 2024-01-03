import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch

# Step 1: Install FAISS library
# pip install faiss-cpu (or faiss-gpu if you have a GPU)

# Step 2: Preprocess the given string
query = input("")
# Perform any necessary preprocessing such as removing stopwords or lowercasing

# Step 3: Convert the string to an embedding
tokenizer = AutoTokenizer.from_pretrained("text-embedding-ada-002")
model = AutoModel.from_pretrained("text-embedding-ada-002")

inputs = tokenizer(query, return_tensors="pt")
outputs = model(**inputs)
query_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Step 4: Perform a similarity search in the FAISS index

# Assuming you already have a populated FAISS index:
# index = faiss.IndexFlatL2(dimension)  # dimension should match your embedding size

indexFilePath = "something.index"
index = faiss.read_index(indexFilePath)

# Perform the search
k = 10  # Number of search results to return
distances, indices = index.search(query_embedding, k)

# `indices` contains the indices of the k most similar items
# `distances` contains the corresponding squared L2 distances
