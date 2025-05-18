# agents/base_agent.py

from core.llm_interface import LLM

class BaseAgent:
    def __init__(self, role_name: str, system_prompt: str):
        self.role_name = role_name
        self.system_prompt = system_prompt
        self.llm = LLM()

    def generate_prompt(self, user_input: str, context: str = "") -> str:
        return f"""{self.system_prompt}

[Context]
{context}

[User Input]
{user_input}
"""

    def respond(self, user_input: str, context: str = "") -> str:
        prompt = self.generate_prompt(user_input, context)
        return self.llm.complete(prompt)
