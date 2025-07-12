
# 🚀 StartMind — AI Co-Founder CLI/TUI Agent Suite

**StartMind** is an LLM-powered multi-agent system designed to act as your AI co-founder. It supports startup ideation, product planning, tech stack decisions, and funding strategy — all from a terminal interface. It features intelligent agent selection, contextual RAG-based retrieval, persistent memory, and a seamless CLI/TUI interface built for developers.

---

## 🌟 Features

- 🧠 **Multi-Agent Architecture**
  - `PMAgent` – Advises on features, user flows, and roadmaps.
  - `CTOAgent` – Recommends tech stacks, architectures, and APIs.
  - `InvestorAgent` – Evaluates funding strategies, valuation, and pitches.

- 📚 **RAG-Backed Context**
  - Retrieves relevant startup knowledge using FAISS + OpenAI embeddings.
  - Supports PDF, Markdown, and text-based sources.

- 🧠 **Memory System**
  - JSON-based memory logs store user & agent interactions across sessions.

- 🔄 **MCP Layer (Modular Cognitive Process)**
  - Retrieves memory and context for each prompt.
  - Automatically selects the most relevant agent.

- 🖥 **TUI Mode (Textual)**
  - Terminal-based interface using `Textual`.
  - Keeps the look and feel of PowerShell/CMD.

- 🧪 **CLI Mode**
  - Full session control via keyboard with history logging.
  - Ideal for devs who prefer terminal-based workflows.

---

## 📁 Project Structure

```
startmind/
├── agents/
│   ├── base_agent.py
│   ├── cto_agent.py
│   ├── pm_agent.py
│   ├── investor_agent.py
│   └── agent.py
│
├── mcp/
│   ├── context_protocol.py
│   ├── memory.py
│   └── controller.py
│
├── rag/
│   ├── retriever.py
│   ├── ingest.py
│   └── sources/
│       ├── lean_startup.pdf
│       ├── yc_notes.md
│       ├── tech_stacks.md
│       └── sample_mvp_readmes/
│
├── core/
│   ├── llm_interface.py
│   ├── config.py
│  
│
├── sessions/
│   └── memory_db.json
│
├── tui/
│   ├── app.py
│   └── styles.css
│
├── main.py
├── cli.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 📦 Setup

```bash
git clone https://github.com/yourname/startmind.git
cd startmind
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 🔑 Add Your OpenAI API Key

Create a `.env` file in the root folder:

```
OPENAI_API_KEY=your-key-here
```

Or export it manually in your terminal.

---

## 📥 RAG Setup (Document Embedding)

Run this script once to embed all documents for semantic retrieval:

```bash
python rag/ingest.py
```

This:
- Splits your documents
- Embeds them using OpenAI embeddings
- Saves a FAISS index to `rag/index/`

---

## 🚀 Running StartMind

### 🧑‍💻 CLI Mode (for devs)

```bash
python cli.py
```

- Load or create sessions
- Memory and RAG-enhanced agent responses
- Chat-style prompt-response loop
- Full session logging

### 💻 TUI Mode (Textual)

```bash
python tui/app.py
```

- Terminal-native interface
- Editable input bar + scrollable output
- Built with [`Textual`](https://textual.textualize.io/)

---

## 🧠 How It Works

1. You enter a prompt.
2. **MCP layer**:
   - Selects relevant agent based on intent
   - Pulls similar document chunks using FAISS
   - Adds recent memory from session
3. The agent:
   - Builds a role-specific prompt
   - Sends it to OpenAI via LangChain
4. Response is printed & saved to history.

---

## ✅ Current Capabilities

- [x] LLM integration with OpenAI
- [x] Document embedding via FAISS
- [x] JSON memory across sessions
- [x] MCP for persisting context and system prompts across the agents while running.
- [x] RAG for real-time retrieval of documents, pdfs, etc added during the ingestion phase.   
- [x] Agent architecture and prompt templating
- [x] CLI interface
- [x] TUI via Textual
- [x] Auto-agent selection via intent routing

---

## 🧪 Sample Prompts

Try these to test agent routing:

- `I'm building a fintech app for Gen Z. What features should be in the MVP?`
- `What stack should I use to launch a SaaS product fast?`
- `How do I convince investors my LTV/CAC ratio is solid?`
- `Suggest a tech architecture for a scalable chat app.`
- `Give me a roadmap for a mental health startup.`

---

## 🔮 Future Roadmap

- [ ] Vector memory for long-term agent learning
- [ ] Agent-to-agent conversations
- [ ] MCP Plugin/tool support
- [ ] User interface for non-developers (dashboard or exportable summary)
- [ ] PDF investor reports and product documentation export

---

## 🤝 Contributing

This is a personal learning + demonstration project, but feel free to fork, explore, or build on top of it. PRs and ideas are welcome!

---

## 📚 Tech Stack

- 🧠 [LangChain](https://github.com/langchain-ai/langchain)
- 🔍 [FAISS](https://github.com/facebookresearch/faiss)
- 💬 [OpenAI API](https://platform.openai.com/)
- 🖥 [Textual (for TUI)](https://textual.textualize.io/)
- 📖 [Unstructured](https://github.com/Unstructured-IO/unstructured)

---

## 📜 License

MIT License

---


### 🚀 Built with ❤️ by [Raghav Kavimandan](https://github.com/yourgithubusername)
