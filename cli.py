import os
import json
import datetime

from mcp.context_protocol import MCP
from agents.agent import Agent
from rag.retriever import Retriever
from mcp.memory import Memory

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

def select_agent():
    # For demo: hardcoded agents, you can expand dynamically
    agents = {
        "1": "CTOAgent",
        "2": "PMAgent",
        "3": "InvestorAgent"
    }
    print("\nChoose an agent:")
    for k, v in agents.items():
        print(f"{k}: {v}")
    choice = input("Agent number: ").strip()
    return agents.get(choice, "CTOAgent")

def main():
    print("=== Welcome to StartMind CLI ===\n")

    # List existing sessions
    sessions = list_sessions()
    if sessions:
        print("Existing sessions:")
        for i, s in enumerate(sessions, 1):
            print(f"{i}: {s}")
    else:
        print("No existing sessions found.")

    # Select or create session
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

    # Initialize core components
    retriever = Retriever()
    memory_store = Memory()
    context_protocol = MCP(memory_store, retriever)

    # Main loop
    print("\nType 'exit' to quit, 'history' to view session history.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        elif user_input.lower() == "history":
            if not history:
                print("No history yet.")
            else:
                for i, item in enumerate(history, 1):
                    print(f"\n[{i}] {item['timestamp']} - Agent: {item['agent']}\nUser: {item['user_input']}\nResponse: {item['llm_response']}")
            continue
        elif user_input == "":
            continue

        agent_name = select_agent()
        agent = Agent(agent_name)

        # Get context with MCP
        context = context_protocol.get_context(user_input)

        # Generate prompt
        prompt = agent.generate_prompt(context, user_input)

        # Call LLM
        llm_response = agent.call_llm(prompt)

        # Show response
        print(f"\n[{agent_name}]: {llm_response}\n")

        # Update memory
        memory_store.add_to_memory(user_input, llm_response)

        # Save to session
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agent": agent_name,
            "user_input": user_input,
            "llm_response": llm_response
        }
        history.append(interaction)
        save_session(session_name, history)

if __name__ == "__main__":
    main()
