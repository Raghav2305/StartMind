# mcp/memory.py

import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings

class VectorMemory:
    def __init__(self, embedding_model="text-embedding-3-large"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.dimension = 1536  # Dimension for text-embedding-3-large
        self.index = faiss.IndexFlatL2(self.dimension)
        self.memory_vectors = []
        self.memory_texts = []

    def log(self, text: str):
        """Adds a text to the memory."""
        vector = self.embeddings.embed_query(text)
        self.index.add(np.array([vector]))
        self.memory_vectors.append(vector)
        self.memory_texts.append(text)

    def get_recent(self, query: str, k: int = 3) -> list[str]:
        """Retrieves the most relevant memories."""
        if not self.memory_texts:
            return []
        
        query_vector = self.embeddings.embed_query(query)
        _, indices = self.index.search(np.array([query_vector]), k)
        
        return [self.memory_texts[i] for i in indices[0] if i < len(self.memory_texts)]

    def add_to_memory(self, user_input: str, agent_response: str):
        """Adds user input and agent response to the memory."""
        self.log(f"User: {user_input}")
        self.log(f"Agent: {agent_response}")

