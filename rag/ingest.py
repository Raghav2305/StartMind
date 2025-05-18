# rag/ingest.py

import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
    return sum([loader.load() for loader in loaders], [])  # flatten

def ingest():
    print("[Ingesting documents...]")
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(INDEX_DIR)
    print(f"[Ingested {len(docs)} chunks into FAISS index]")

if __name__ == "__main__":
    ingest()
