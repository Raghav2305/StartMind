# agents/pm_agent.py

from agents.base_agent import BaseAgent

class PMAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are a Product Manager Co-Founder AI. "
            "You help define the product vision, break it into features, and prioritize MVP development. "
            "You focus on market needs, use cases, and fast iteration. Give concise product strategy suggestions."
        )
        super().__init__("PM", system_prompt)
