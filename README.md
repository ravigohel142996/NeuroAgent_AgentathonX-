# NeuroAgent 🧠

**Multi-Agent AI Command Center** — Research · Plan · Code · Analyse · Report

NeuroAgent is a production-level multi-agent AI system built with **CrewAI** and **Streamlit**.  
It accepts a user task and autonomously orchestrates five specialised AI agents to research,
plan, write code, analyse, and produce a structured final report.

---

## Architecture

```
Streamlit UI
    │
    ▼
Orchestrator
    │
    ├─▶ 📋 Planner Agent    → Breaks task into a numbered action plan
    ├─▶ 🔍 Research Agent   → Gathers background knowledge & best practices
    ├─▶ 💻 Coding Agent     → Writes production-ready code with docs & tests
    ├─▶ 📊 Analysis Agent   → Evaluates outputs, finds risks & opportunities
    └─▶ 📄 Report Agent     → Compiles a comprehensive Markdown report
```

## Project Structure

```
NeuroAgent/
├── app.py                  # Streamlit UI entry point
├── requirements.txt
├── .gitignore
├── src/
│   ├── config.py           # Global configuration (env vars)
│   ├── orchestrator.py     # Pipeline orchestration
│   ├── tasks.py            # CrewAI Task definitions
│   └── agents/
│       ├── research_agent.py
│       ├── planner_agent.py
│       ├── coding_agent.py
│       ├── analysis_agent.py
│       └── report_agent.py
└── utils/
    └── logger.py           # Structured logging
```

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/ravigohel142996/NeuroAgent.git
cd NeuroAgent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini   # optional, default: gpt-4o-mini
TEMPERATURE=0.3             # optional, default: 0.3
```

### 3. Run

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Streamlit Cloud deployment note

If deploying to Streamlit Community Cloud, keep `runtime.txt` in the repo root with the exact format below so Python 3.11 is used (CrewAI requires Python >=3.10):

```
python-3.11
```

---

## Features

| Feature | Details |
|---|---|
| 🤖 5 Specialised Agents | Planner, Researcher, Coder, Analyst, Reporter |
| 🔄 Sequential Pipeline | Outputs from each agent flow into the next |
| 🎨 Modern Dark UI | Gradient cards, live progress indicators |
| 📊 Per-agent results | Expandable output per agent with timing metrics |
| ⬇️ Report download | One-click Markdown report download |
| 📋 Structured logging | Daily rotating log files under `logs/` |
| ⚙️ Sidebar configuration | API key, model, temperature — no restart needed |

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model name |
| `TEMPERATURE` | `0.3` | LLM sampling temperature |
| `MAX_ITERATIONS` | `10` | Max agent iterations per task |
| `VERBOSE_AGENTS` | `false` | Enable verbose CrewAI logging |

## Tech Stack

- [CrewAI](https://github.com/crewAIInc/crewAI) — multi-agent orchestration
- [Streamlit](https://streamlit.io) — interactive web UI
- [LangChain OpenAI](https://github.com/langchain-ai/langchain) — LLM integration
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment management

---

## License

MIT
