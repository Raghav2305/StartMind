# rag/ingest.py

import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_experimental.text_splitter import SemanticChunker
from tqdm import tqdm

DOCS_DIR = "rag/sources"
INDEX_DIR = "rag/index"

def load_documents():
    loaders = []
    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        if file.endswith(".pdf"):
            loaders.append(PyPDFLoader(path))
        elif file.endswith(".md"):
            loaders.append(UnstructuredMarkdownLoader(path))
        elif file.endswith(".txt"):
            loaders.append(TextLoader(path))
    
    documents = []
    for loader in tqdm(loaders, desc="Loading documents"):
        documents.extend(loader.load())
    return documents

def ingest():
    print("[Ingesting documents...]")
    documents = load_documents()

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    splitter = SemanticChunker(embeddings)
    docs = splitter.split_documents(documents)

    print(f"Splitting {len(documents)} documents into {len(docs)} chunks.")

    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(tqdm(docs, desc="Embedding documents"), embeddings)

    vectorstore.save_local(INDEX_DIR)
    print(f"[Ingested {len(docs)} chunks into FAISS index]")

if __name__ == "__main__":
    ingest()
