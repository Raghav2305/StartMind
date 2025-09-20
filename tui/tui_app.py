# tui/tui_app.py

import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import datetime

from textual.app import App, ComposeResult
from textual.widgets import Input, Static, Header, Footer
from textual.containers import VerticalScroll, Container
from textual.reactive import reactive

from mcp.context_protocol import MCP
from agents.cto_agent import CTOAgent
from agents.pm_agent import PMAgent
from agents.investor_agent import InvestorAgent
from rag.retriever import Retriever
from mcp.memory import VectorMemory

SESSIONS_DIR = "sessions"

class StartMindTUI(App):
    CSS_PATH = "styles.css" # Link to a separate CSS file for styling

    user_input = reactive("")
    session_name = ""
    history = []
    memory_store = None
    retriever = None
    context_protocol = None
    agents = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Static("Welcome to StartMind! Type your query below.", id="welcome-message"),
            id="chat-display"
        )
        yield Input(placeholder="Ask your AI co-founder...", id="user-input")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#user-input", Input).focus()
        self.initialize_session()

    def initialize_session(self) -> None:
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)

        sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
        
        if sessions:
            self.session_name = sessions[-1]  # Load latest session
            self.history = self.load_session(self.session_name)
            self.query_one("#welcome-message", Static).update(f"Loaded session: {self.session_name}")
            # Pre-fill chat-display with past history
            chat_text = ""
            for entry in self.history:
                chat_text += f"\n\n[bold blue]You:[/bold blue] {entry['user_input']}\n[bold green]{entry['agent']}:[/bold green] {entry['llm_response']}"
            self.query_one("#chat-display", VerticalScroll).mount(Static(chat_text))
        else:
            self.session_name = "startmind_default.json"
            self.history = []
            self.query_one("#welcome-message", Static).update(f"Created new session: {self.session_name}")

        self.retriever = Retriever()
        self.memory_store = VectorMemory()
        self.context_protocol = MCP(self.memory_store, self.retriever)

        self.agents = {
            "CTOAgent": CTOAgent(),
            "PMAgent": PMAgent(),
            "InvestorAgent": InvestorAgent()
        }

    def load_session(self, name):
        path = os.path.join(SESSIONS_DIR, name)
        with open(path, "r") as f:
            return json.load(f)

    def save_session(self) -> None:
        path = os.path.join(SESSIONS_DIR, self.session_name)
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)

    def append_message(self, sender: str, message: str, agent_name: str = "") -> None:
        chat_display = self.query_one("#chat-display", VerticalScroll)
        if sender == "You":
            chat_display.mount(Static(f"\n\n[bold blue]You:[/bold blue] {message}"))
        else:
            chat_display.mount(Static(f"\n[bold green]{agent_name}:[/bold green] {message}"))
        chat_display.scroll_end()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()
        self.query_one("#user-input", Input).value = ""

        if not user_input:
            return

        self.append_message("You", user_input)

        agent_name = self.context_protocol.select_agents(user_input)[0]
        agent = self.agents.get(agent_name)
        if not agent:
            self.append_message("System", f"Error: Agent '{agent_name}' not found.")
            return

        try:
            context = self.context_protocol.get_context(user_input)
            memory_context = self.memory_store.get_recent(user_input)
            newline_char = chr(10) # Using chr(10) to avoid f-string backslash issues
            full_context = f"{context}{newline_char}{newline_char}Recent Memory:{newline_char}{newline_char.join(memory_context)}"
            
            llm_response = agent.respond(user_input, full_context)

            self.append_message("Agent", llm_response, agent_name)

            self.memory_store.add_to_memory(user_input, llm_response)
            self.history.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "agent": agent_name,
                "user_input": user_input,
                "llm_response": llm_response,
            })
            self.save_session()

        except Exception as e:
            self.append_message("System", f"Error running {agent_name}: {e}")
            import traceback
            traceback.print_exc() # Print traceback to console for debugging

if __name__ == "__main__":
    StartMindTUI().run()
