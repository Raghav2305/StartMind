# mcp/context_protocol.py

from rag.retriever import Retriever
from mcp.memory import VectorMemory
from core.llm_interface import call_llm

class MCP:
    def __init__(self, memory: VectorMemory, retriever: Retriever):
        self.memory = memory
        self.retriever = retriever
        self.agent_selection_prompt = """
Given the user input, select the most appropriate agent to respond. The available agents are:
- CTOAgent: For technical questions about technology stacks, architecture, and APIs.
- PMAgent: For product-related questions about features, roadmaps, and user stories.
- InvestorAgent: For business and funding-related questions about investment, valuation, and pitch decks.

User input: "{user_input}"

Return only the name of the agent, e.g., "CTOAgent".
"""

    def _get_agent_from_llm(self, user_input: str) -> str:
        """Selects an agent using an LLM call."""
        prompt = self.agent_selection_prompt.format(user_input=user_input)
        agent_name = call_llm(prompt, model="gpt-3.5-turbo").strip()
        
        # Ensure the returned agent name is one of the valid agents
        if agent_name not in ["CTOAgent", "PMAgent", "InvestorAgent"]:
            return "PMAgent" # Default fallback
        return agent_name

    def select_agents(self, user_input: str) -> list[str]:
        """Selects agents based on user input using an LLM."""
        agent_name = self._get_agent_from_llm(user_input)
        return [agent_name]

    def get_context(self, user_input: str) -> str:
        """Use RAG to provide additional documents."""
        docs = self.retriever.get_relevant_docs(user_input)
        return "\n".join([doc.page_content for doc in docs])
