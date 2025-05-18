# mcp/controller.py

from agents.cto_agent import CTOAgent
from agents.pm_agent import PMAgent
from agents.investor_agent import InvestorAgent
from mcp.memory import Memory
from mcp.context_protocol import MCP

class Controller:
    def __init__(self):
        self.memory = Memory()
        self.mcp = MCP()
        self.agents = {
            "CTO": CTOAgent(),
            "PM": PMAgent(),
            "INVESTOR": InvestorAgent()
        }

    def route(self, user_input):
        self.memory.log_user(user_input)

        selected_agents = self.mcp.select_agents(user_input)
        rag_context = self.mcp.get_context(user_input)

        responses = {}

        for role in selected_agents:
            memory_context = self.memory.get_recent(role)
            full_context = memory_context + "\n" + rag_context
            reply = self.agents[role].respond(user_input, full_context)
            self.memory.log_agent(role, reply)
            responses[role] = reply

        return responses
