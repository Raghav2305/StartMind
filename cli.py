import os
import json
import datetime
import sys

from mcp.context_protocol import MCP
from agents.agent import Agent
from rag.retriever import Retriever
from mcp.memory import VectorMemory

SESSIONS_DIR = "sessions"

def list_sessions():
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)
    files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    return files

def load_session(session_name):
    path = os.path.join(SESSIONS_DIR, session_name)
    if not os.path.exists(path):
        print(f"Session '{session_name}' not found.")
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_session(session_name, data):
    path = os.path.join(SESSIONS_DIR, session_name)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("=== Welcome to StartMind CLI ===\n")

    sessions = list_sessions()
    if sessions:
        print("Existing sessions:")
        for i, s in enumerate(sessions, 1):
            print(f"{i}: {s}")
    else:
        print("No existing sessions found.")

    session_name = ""
    history = []

    if sys.stdin.isatty():
        # Interactive mode
        session_choice = input("Enter session number to load or press Enter to create new: ").strip()
        if session_choice and session_choice.isdigit() and 1 <= int(session_choice) <= len(sessions):
            session_name = sessions[int(session_choice) - 1]
            history = load_session(session_name)
            print(f"Loaded session '{session_name}' with {len(history)} entries.")
        else:
            session_name = input("Enter new session name (e.g., 'fintech_project.json'): ").strip()
            if not session_name.endswith(".json"):
                session_name += ".json"
            history = []
            print(f"Created new session '{session_name}'.")
    else:
        # Non-interactive mode
        if sessions:
            session_name = sessions[-1] # Load latest session
            history = load_session(session_name)
            print(f"Loaded session: {session_name}")
        else:
            session_name = "startmind_default.json"
            history = []
            print(f"Created new session: {session_name}")

    # Initialize core components
    retriever = Retriever()
    memory_store = VectorMemory()
    context_protocol = MCP(memory_store, retriever)

    # Main loop
    if sys.stdin.isatty():
        print("\nType 'exit' to quit, 'history' to view session history.\n")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break
            process_input(user_input, context_protocol, memory_store, history, session_name)
    else:
        for user_input in sys.stdin:
            user_input = user_input.strip()
            if not user_input:
                continue
            print(f"You: {user_input}")
            process_input(user_input, context_protocol, memory_store, history, session_name)

def process_input(user_input, context_protocol, memory_store, history, session_name):
    if user_input.lower() == "history":
        if not history:
            print("No history yet.")
        else:
            for i, item in enumerate(history, 1):
                print(f"\n[{i}] {item['timestamp']} - Agent: {item['agent']}\nUser: {item['user_input']}\nResponse: {item['llm_response']}")
        return

    # Automatically select agents using MCP
    agent_roles = context_protocol.select_agents(user_input)
    if not agent_roles:
        print("No relevant agents found for the input. Try rephrasing.")
        return

    for agent_name in agent_roles:
        agent = Agent(agent_name)

        try:
            # Retrieve context and memory
            context = context_protocol.get_context(user_input)
            memory_context = memory_store.get_recent(user_input)
            memory_str = "\n".join(memory_context)
            full_context = f"{context}\n\nRecent Memory:\n{memory_str}"

            # Generate prompt and get LLM response
            prompt = agent.generate_prompt(full_context, user_input)
            llm_response = agent.call_llm(prompt)

            print(f"\n[{agent_name}]: {llm_response}\n")

            # Update memory and save session
            memory_store.add_to_memory(user_input, llm_response)

            interaction = {
                "timestamp": datetime.datetime.now().isoformat(),
                "agent": agent_name,
                "user_input": user_input,
                "llm_response": llm_response
            }
            history.append(interaction)

        except Exception as e:
            print(f"Error running {agent_name}: {e}")

    save_session(session_name, history)

if __name__ == "__main__":
    main()
