# agents/investor_agent.py

from agents.base_agent import BaseAgent

class InvestorAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are a startup investor AI. "
            "Evaluate startup pitches from the perspective of a seed-stage VC. "
            "Assess team, market size, idea, and traction. Ask questions or give feedback like an investor would."
        )
        super().__init__("Investor", system_prompt)
