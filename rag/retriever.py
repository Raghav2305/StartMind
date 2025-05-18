# rag/retriever.py

import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class Retriever:
    def __init__(self, index_dir="rag/index"):
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

    def get_relevant_docs(self, query: str, k=3):
        return self.vectorstore.similarity_search(query, k=k)
