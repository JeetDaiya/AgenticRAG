# AGENTIC_RAG

> A multi-agent AI system that answers complex financial queries by intelligently orchestrating a RAG pipeline, live stock market data, and real-time web search — all in parallel.

> NOTE : This is just a learning project, where I was exploring how to build things with LangGraph, LangChain and LangSmith.

---

## ✨ Features

- 📚 **RAG Pipeline** — Queries the **Wells Fargo 2025 Annual Report** stored in a FAISS vector database using Max Marginal Relevance search
- 📈 **Live Stock Data** — Fetches real-time stock price, market cap, P/E ratio, and 52-week range via **Yahoo Finance**
- 🌐 **Web Intelligence** — Searches the live internet for recent news and events using the **Tavily Search API**
- ⚡ **Parallel Execution** — All three data sources can fire **simultaneously** using LangGraph's fan-out architecture
- 🧠 **Intelligent Routing** — An LLM planner decomposes multi-part queries and routes each part to the right tool automatically
- 📋 **Structured Reports** — Final output is a validated **Pydantic model** with distinct sections for RAG, market, and web data
- 🔄 **Self-Correcting RAG** — Includes an automatic query rewrite loop (up to 3 attempts) if initial retrieval fails

---

## 🗺️ Architecture

```
User Query
    │
    ▼
┌─────────┐
│ Planner │  ← LLM decomposes query, decides which tools to call
└────┬────┘
     │  Conditional Fan-Out (parallel)
     ├──────────────────┬─────────────────────┐
     ▼                  ▼                     ▼
┌──────────┐     ┌────────────┐      ┌──────────────┐
│ RAG Agent│     │ Stock Node │      │  Web Agent   │
│          │     │            │      │              │
│ retrieve │     │  yfinance  │      │ rewrite_for  │
│    ↓     │     │    API     │      │    _web      │
│relevance │     └────────────┘      │     ↓        │
│    ↓     │                         │  get_news    │
│ rewrite  │                         │     ↓        │
│  (loop)  │                         │  formatter   │
└──────────┘                         └──────────────┘
     │                  │                     │
     └──────────────────┴─────────────────────┘
                        │  Fan-In (merge)
                        ▼
                 ┌────────────┐
                 │  Generate  │  ← Final LLM synthesizes into FinalReport
                 └────────────┘
                        │
                        ▼
              Structured Final Report
        (RAG section | Market section | Web section)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Graph Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM Provider | [OpenRouter](https://openrouter.ai) via `langchain-openrouter` (pluggable via `agent/core/model.py`) |
| Vector Database | FAISS + `langchain-community` |
| Embeddings | `BAAI/bge-small-en-v1.5` via `langchain-huggingface` |
| Stock Data | `yfinance` |
| Web Search | [Tavily](https://tavily.com) |
| Structured Output | Pydantic v2 |

---

## 📂 Project Structure

```
Agentic_RAG/
│
├── main.py                          # Entry point — interactive REPL loop
├── draw_graph.py                    # Utility to render graph as PNG
│
├── faiss_data/                      # Pre-built FAISS vector index
│
├── utils/
│   └── format_document_list.py      # Document formatting helper
│
└── agent/
    ├── core/
    │   ├── model.py                 # 🔌 Swap your LLM provider here
    │   ├── shared_state.py          # Master LangGraph state schema
    │   └── pydantic_models/
    │       ├── report_model.py      # FinalReport output schema
    │       └── relevance_response_model.py
    │
    ├── tools/
    │   └── stock_info.py            # yfinance tool wrapper
    │
    ├── orchestrator/
    │   ├── prompt.py                # Planner + Generator system prompts
    │   ├── core/graph.py            # Master graph assembly
    │   └── nodes/
    │       ├── planner.py           # LLM routing brain
    │       ├── router.py            # Conditional fan-out edge
    │       ├── stock.py             # Custom stock state node ✦
    │       └── generate.py          # Final report synthesizer
    │
    └── subgraphs/
        ├── rag_agent/               # Retrieve → Grade → Rewrite loop
        └── web_search_agent/        # Rewrite → Tavily → Format
```

> ✦ `agent/orchestrator/nodes/stock.py` was fully AI-generated. It bridges LangGraph's tool call ID system with the custom `stock_info` state key.

---

## 🚀 Getting Started

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd Agentic_RAG
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
# LLM Provider
OPENROUTER_API_KEY=your_openrouter_api_key

# Web Search
TAVILY_API_KEY=your_tavily_api_key
```

> 💡 Get a **free OpenRouter API key** at [openrouter.ai/keys](https://openrouter.ai/keys) — access hundreds of free and paid models with a single key.  
> 💡 Get a **free Tavily API key** at [tavily.com](https://tavily.com).

### 3. Configure your LLM (`agent/core/model.py`)

This project uses **[OpenRouter](https://openrouter.ai)** — a unified API that gives you access to hundreds of models (free & paid) with a single key.

```python
from langchain_openrouter import ChatOpenRouter
import os

model = ChatOpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-super-120b-a12b:free",  # swap any OpenRouter model here
)
```

> 💡 Browse all available models at [openrouter.ai/models](https://openrouter.ai/models). Free models are marked with `:free`.

### 4. Run

```bash
python main.py
```

---

## 💬 Example Queries

```
👤 What is Wells Fargo's net income from the 2025 annual report?
   → Triggers: RAG only

👤 What is Apple's current stock price and market cap?
   → Triggers: Stock only

👤 What's the latest news about Tesla's CEO?
   → Triggers: Web only

👤 Compare Wells Fargo's 2025 net income to their live stock price today (WFC).
   → Triggers: RAG + Stock (parallel)

👤 What is the live stock price of Tesla (TSLA) and what news is driving performance?
   → Triggers: Stock + Web (parallel)

👤 Give me a comprehensive breakdown of Wells Fargo — annual financials, live stock, and latest news.
   → Triggers: RAG + Stock + Web (all three, parallel)
```

---

## 📊 Sample Output

```
============================================================
📋 FINAL SYNTHESIZED REPORT
============================================================

📚 [2025 Annual Report Analysis]
Wells Fargo reported a net income of $19.7B for fiscal year 2025...

📈 [Live Market Performance]
- Current Price: $75.81 USD
- Market Cap: $231.99B
- 52-Week Range: $71.90 – $97.76
- Analyst Recommendation: Buy

🌐 [Recent Web Intelligence]
## Latest Wells Fargo News
* CEO Charlie Scharf to be appointed as Chairman of the Board...
* Return on tangible common equity improved from 8% to 14%...

🧠 [Executive Summary]
Wells Fargo demonstrates strong fundamental performance with a net income
of $19.7B in 2025, while the stock currently trades at $75.81...
============================================================
```

---

## 🔧 Visualize the Graph

Generate a PNG diagram of the full agent graph topology:

```bash
python draw_graph.py
# Saves: orchestrator_graph.png
```

---

## ⚠️ Known Limitations

- The RAG knowledge base is scoped to the **Wells Fargo 2025 Annual Report** only
- Groq-hosted Llama 3 models have a known XML parser bug with complex structured outputs
- Free models on OpenRouter may have inconsistent tool-calling support — if you see structured output errors, try a more capable model (e.g. `google/gemini-flash-1.5` or `mistralai/mixtral-8x7b-instruct`) via OpenRouter
- The system runs **without persistent memory** — each query starts with a fresh state

---

## 📄 License

MIT License — feel free to use, modify, and extend.
