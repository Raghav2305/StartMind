# mcp/memory.py

import json
import os
from datetime import datetime

class Memory:
    def __init__(self, memory_path="sessions/memory_db.json"):
        self.path = memory_path
        self.memory = self.load()

    def load(self):
        if not os.path.exists(self.path):
            return {"user": [], "agents": {}}
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def log_user(self, text):
        self.memory["user"].append({"timestamp": str(datetime.now()), "text": text})
        self.save()

    def log_agent(self, role, text):
        if role not in self.memory["agents"]:
            self.memory["agents"][role] = []
        self.memory["agents"][role].append({"timestamp": str(datetime.now()), "text": text})
        self.save()

    def get_recent(self, role=None, limit=3):
        if role and role in self.memory["agents"]:
            return "\n".join([msg["text"] for msg in self.memory["agents"][role][-limit:]])
        return "\n".join([msg["text"] for msg in self.memory["user"][-limit:]])
    
    def add_to_memory(self, user_input, agent_response, agent_role="agent"):
        self.log_user(user_input)
        self.log_agent(agent_role, agent_response)

