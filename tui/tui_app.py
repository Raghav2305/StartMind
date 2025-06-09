# tui/app.py

import os
import json
import datetime

from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical
from textual.reactive import reactive
from textual.scroll_view import ScrollView

from mcp.context_protocol import MCP
from agents.agent import Agent
from rag.retriever import Retriever
from mcp.memory import Memory

SESSIONS_DIR = "sessions"


class StartMindTUI(App):
    CSS = """
    #chat_output {
    background: $background;
    color: $text;
    border: round white;
    padding: 1 2;
    height: 1fr;
    overflow: auto;
}

#input {
    border: round green;
    background: $panel;
    color: $text;
    padding: 1 1;
}

#welcome {
    content-align: center middle;
    color: yellow;
    height: auto;
    padding: 1;
}

#session_loader {
    color: cyan;
    padding-left: 2;
}


    """

    user_input = reactive("")
    session_name = ""
    history = []
    memory_store = None
    retriever = None
    context_protocol = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("", id="session_loader"),
            ScrollView(Static("", id="chat_output"), id="scroll_area"),
            Static("> ", id="prompt"),
            Input(placeholder="", id="input"),
        )

    def on_mount(self) -> None:
        self.query_one("#chat_output", Static).update("")
        self.initialize_session()
        # Autofocus input
        self.set_focus(self.query_one("#input"))

    def initialize_session(self) -> None:
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)

        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
        session_loader = self.query_one("#session_loader", Static)

        if sessions:
            self.session_name = sessions[-1]  # Load latest session
            self.history = self.load_session(self.session_name)
            session_loader.update(f"Loaded session: {self.session_name}")
            # Pre-fill chat_output with past history
            chat_text = ""
            for entry in self.history:
                chat_text += f"\n\nYou: {entry['user_input']}\n[{entry['agent']}]: {entry['llm_response']}"
            self.query_one("#chat_output", Static).update(chat_text)
        else:
            self.session_name = "startmind_default.json"
            self.history = []
            session_loader.update(f"Created new session: {self.session_name}")

        self.retriever = Retriever()
        self.memory_store = Memory()
        self.context_protocol = MCP(self.memory_store, self.retriever)

    def load_session(self, name):
        path = os.path.join(SESSIONS_DIR, name)
        with open(path, "r") as f:
            return json.load(f)

    def save_session(self):
        path = os.path.join(SESSIONS_DIR, self.session_name)
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)

    def append_output(self, user, agent, response):
        output = self.query_one("#chat_output", Static)
        prev = output.renderable or ""
        new = f"{prev}\n\nYou: {user}\n[{agent}]: {response}"
        output.update(new)
        self.query_one("#scroll_area", ScrollView).scroll_end()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        self.user_input = event.value.strip()
        self.query_one("#input", Input).value = ""

        if not self.user_input:
            return

        agent_name = self.auto_select_agent(self.user_input)
        agent = Agent(agent_name)

        context = self.context_protocol.get_context(self.user_input)
        prompt = agent.generate_prompt(context, self.user_input)
        llm_response = agent.call_llm(prompt)

        self.append_output(self.user_input, agent_name, llm_response)

        self.memory_store.add(user_query=self.user_input, agent_response=llm_response)
        self.history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": agent_name,
            "user_input": self.user_input,
            "llm_response": llm_response,
        })
        self.save_session()

    def auto_select_agent(self, prompt):
        prompt = prompt.lower()
        if "feature" in prompt or "design" in prompt or "mvp" in prompt:
            return "PMAgent"
        elif "invest" in prompt or "fund" in prompt or "valuation" in prompt:
            return "InvestorAgent"
        else:
            return "CTOAgent"


if __name__ == "__main__":
    StartMindTUI().run()
