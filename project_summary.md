
# Project Summary: StartMind

StartMind is an AI-powered multi-agent system that acts as a co-founder for startups. It provides guidance on product management, technology stacks, and investment strategies. The system is designed with a modular architecture, allowing for easy expansion and maintenance.

## Core Components

### 1. Agents
The system is composed of three specialized agents:
- **PMAgent**: Advises on product features, roadmaps, and MVP scope.
- **CTOAgent**: Recommends technology stacks, architecture, and APIs.
- **InvestorAgent**: Provides insights into funding strategies, valuation, and investor pitches.

Each agent is built upon a `BaseAgent` class, which provides a common interface for interacting with the language model.

### 2. Modular Cognitive Process (MCP)
The MCP layer is the central controller of the system. It is responsible for:
- **Agent Selection**: It uses a keyword-based approach to select the most appropriate agent for a given user query.
- **Context Retrieval**: It retrieves relevant documents from the RAG system to provide context to the agents.
- **Memory Management**: It interacts with the memory system to maintain a history of interactions.

### 3. Retrieval-Augmented Generation (RAG)
The RAG system enhances the agents' knowledge by providing them with relevant information from a collection of documents. It uses a FAISS vector store to perform similarity searches and retrieve the most relevant document chunks. The `ingest.py` script is used to process and index the documents.

### 4. Memory
The memory system persists the conversation history in JSON files. This allows the system to maintain context across sessions. The `Memory` class provides methods for logging user inputs and agent responses.

### 5. User Interfaces
StartMind provides two user interfaces:
- **CLI (Command-Line Interface)**: A simple and intuitive interface for developers who prefer to work in the terminal.
- **TUI (Text-based User Interface)**: A more interactive and user-friendly interface built with the `Textual` library.

## Workflows

### 1. Initialization
- The user starts the application through either the CLI or the TUI.
- The system loads an existing session or creates a new one.
- The core components (MCP, RAG, Memory) are initialized.

### 2. User Interaction
- The user enters a query.
- The MCP layer selects the most appropriate agent(s) based on the query.
- The MCP layer retrieves relevant context from the RAG system and recent memory.
- The selected agent generates a prompt that includes the system prompt, the retrieved context, and the user's query.
- The agent sends the prompt to the language model and receives a response.
- The response is displayed to the user.
- The interaction is logged to the memory system.

### 3. RAG Ingestion
- The `rag/ingest.py` script is run to process and index the documents in the `rag/sources` directory.
- The script loads the documents, splits them into chunks, generates embeddings, and stores them in a FAISS index.

## Activity Log

- **2025-09-20**:
    - Analyzed the project structure and file contents.
    - Read the `README.md` file to understand the project's purpose and features.
    - Examined the core components of the application, including the agents, MCP, RAG, and memory systems.
    - Created this `project_summary.md` file to document the project's architecture and workflows.
