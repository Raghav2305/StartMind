# mcp/context_protocol.py

from rag.retriever import Retriever
from mcp.memory import Memory

class MCP:
    def __init__(self, memory: Memory, retriever: Retriever):
        self.memory = memory
        self.retriever = retriever

    def select_agents(self, user_input):
        """Naive selector for now — later use keyword/topic modeling."""
        agents = []
        if any(word in user_input.lower() for word in ["tech", "stack", "architecture", "api"]):
            agents.append("CTO")
        if any(word in user_input.lower() for word in ["feature", "roadmap", "mvp", "users"]):
            agents.append("PM")
        if any(word in user_input.lower() for word in ["fund", "invest", "pitch", "valuation"]):
            agents.append("INVESTOR")
        return agents or ["PM"]  # Default fallback

    def get_context(self, user_input):
        """Use RAG to provide additional documents."""
        docs = self.retriever.get_relevant_docs(user_input)
        return "\n".join([doc.page_content for doc in docs])
