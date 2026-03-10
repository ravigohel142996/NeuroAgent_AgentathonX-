"""NeuroAgent – Streamlit UI entry point."""

from __future__ import annotations

import os
import sys
import time
from typing import Optional

import streamlit as st

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path so relative imports work when the app is
# launched with `streamlit run app.py` from any working directory.
# ---------------------------------------------------------------------------
_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils.logger import get_logger  # noqa: E402

logger = get_logger("app")

# ---------------------------------------------------------------------------
# Page config (must be the very first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NeuroAgent – Multi-Agent AI Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS – modern dark-themed UI
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---- Global ---- */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        color: #e0e0e0;
    }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0e1117 100%);
        border-right: 1px solid #2a2f3e;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: opacity 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.85;
        color: white;
    }

    /* ---- Cards ---- */
    .agent-card {
        background: #1e2130;
        border: 1px solid #2a2f3e;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.3s ease;
    }
    .agent-card.active  { border-color: #7c3aed; }
    .agent-card.done    { border-color: #22c55e; }
    .agent-card.failed  { border-color: #ef4444; }

    /* ---- Progress bar ---- */
    .stProgress > div > div { background-color: #7c3aed; }

    /* ---- Text area ---- */
    textarea { background-color: #1e2130 !important; color: #e0e0e0 !important; }

    /* ---- Report box ---- */
    .report-box {
        background: #1e2130;
        border: 1px solid #2a2f3e;
        border-radius: 12px;
        padding: 1.5rem 2rem;
    }

    /* ---- Hero ---- */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .hero-sub {
        color: #6b7280;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Agent metadata
# ---------------------------------------------------------------------------
AGENTS = [
    {
        "id": "Planner",
        "icon": "📋",
        "title": "Planner Agent",
        "description": "Decomposes the task into a prioritised action plan.",
    },
    {
        "id": "Researcher",
        "icon": "🔍",
        "title": "Research Agent",
        "description": "Gathers background knowledge, best practices, and references.",
    },
    {
        "id": "Coder",
        "icon": "💻",
        "title": "Coding Agent",
        "description": "Produces production-ready code with docstrings and examples.",
    },
    {
        "id": "Analyst",
        "icon": "📊",
        "title": "Analysis Agent",
        "description": "Evaluates all outputs for risks, gaps, and opportunities.",
    },
    {
        "id": "Reporter",
        "icon": "📄",
        "title": "Report Agent",
        "description": "Compiles a structured Markdown report from all findings.",
    },
]

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
def _init_state() -> None:
    defaults = {
        "running": False,
        "agent_statuses": {a["id"]: "idle" for a in AGENTS},
        "agent_messages": {a["id"]: "" for a in AGENTS},
        "pipeline_result": None,
        "error_message": None,
        "run_count": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_state()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        placeholder="sk-…",
        help="Your OpenAI API key. Stored only for this session.",
    )
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input

    model_choice = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
    )
    os.environ["OPENAI_MODEL"] = model_choice

    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
    os.environ["TEMPERATURE"] = str(temperature)

    st.markdown("---")
    st.markdown("### 🤖 Pipeline Overview")
    for agent in AGENTS:
        st.markdown(f"**{agent['icon']} {agent['title']}**")
        st.caption(agent["description"])

    st.markdown("---")
    st.caption("NeuroAgent v1.0 · Powered by CrewAI & OpenAI")


# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.markdown('<p class="hero-title">🧠 NeuroAgent</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Multi-Agent AI Command Center – Research · Plan · Code · Analyse · Report</p>',
    unsafe_allow_html=True,
)

# Task input
task_input = st.text_area(
    "Describe your task",
    height=120,
    placeholder=(
        "e.g. Build a REST API for a todo application using FastAPI and PostgreSQL, "
        "including authentication and unit tests."
    ),
    key="task_input",
)

col_run, col_clear = st.columns([3, 1])
with col_run:
    run_button = st.button("🚀 Run Agents", disabled=st.session_state.running)
with col_clear:
    clear_button = st.button("🗑️ Clear", disabled=st.session_state.running)

if clear_button:
    st.session_state.pipeline_result = None
    st.session_state.error_message = None
    st.session_state.agent_statuses = {a["id"]: "idle" for a in AGENTS}
    st.session_state.agent_messages = {a["id"]: "" for a in AGENTS}
    st.rerun()

# ---------------------------------------------------------------------------
# Agent progress panel
# ---------------------------------------------------------------------------
st.markdown("### 🤖 Agent Progress")
agent_cols = st.columns(len(AGENTS))
agent_placeholders = {}
for i, agent in enumerate(AGENTS):
    with agent_cols[i]:
        agent_placeholders[agent["id"]] = st.empty()


def _render_agent_card(placeholder, agent: dict, status: str, message: str) -> None:
    css_class = {"idle": "", "active": "active", "done": "done", "failed": "failed"}.get(
        status, ""
    )
    spinner = {"idle": "⬜", "active": "🔄", "done": "✅", "failed": "❌"}.get(status, "⬜")
    msg_html = f"<small style='color:#9ca3af'>{message}</small>" if message else ""
    placeholder.markdown(
        f"""
        <div class="agent-card {css_class}">
            <div style="font-size:1.5rem">{agent['icon']}</div>
            <strong>{agent['title']}</strong><br/>
            <span style="font-size:0.85rem;color:#9ca3af">{spinner} {status.capitalize()}</span>
            {msg_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Render initial state
for agent in AGENTS:
    _render_agent_card(
        agent_placeholders[agent["id"]],
        agent,
        st.session_state.agent_statuses[agent["id"]],
        st.session_state.agent_messages[agent["id"]],
    )

# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------
if run_button:
    task_text = (task_input or "").strip()
    if not task_text:
        st.warning("⚠️ Please enter a task before running the agents.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("🔑 Please provide your OpenAI API key in the sidebar.")
    else:
        st.session_state.running = True
        st.session_state.pipeline_result = None
        st.session_state.error_message = None
        st.session_state.agent_statuses = {a["id"]: "idle" for a in AGENTS}
        st.session_state.agent_messages = {a["id"]: "" for a in AGENTS}

        progress_bar = st.progress(0, text="Initialising pipeline…")
        total_steps = len(AGENTS)

        def progress_callback(agent_name: str, status_msg: str) -> None:
            # Mark previous agents as done
            idx = next((i for i, a in enumerate(AGENTS) if a["id"] == agent_name), None)
            if idx is not None:
                for a in AGENTS[:idx]:
                    st.session_state.agent_statuses[a["id"]] = "done"
                st.session_state.agent_statuses[agent_name] = "active"
            st.session_state.agent_messages[agent_name] = status_msg

            # Re-render all cards
            for ag in AGENTS:
                _render_agent_card(
                    agent_placeholders[ag["id"]],
                    ag,
                    st.session_state.agent_statuses[ag["id"]],
                    st.session_state.agent_messages[ag["id"]],
                )

            # Update progress bar
            done_count = sum(
                1
                for a in AGENTS
                if st.session_state.agent_statuses[a["id"]] in ("done", "active")
            )
            progress_bar.progress(
                min(done_count / total_steps, 1.0),
                text=f"Running {agent_name}…",
            )

        try:
            from src.orchestrator import Orchestrator  # lazy import avoids crewai at module load

            orch = Orchestrator(progress_callback=progress_callback)
            logger.info("UI dispatching task to orchestrator | task=%r", task_text)
            pipeline_result = orch.run(task_text)

            if pipeline_result.success:
                for ag in AGENTS:
                    st.session_state.agent_statuses[ag["id"]] = "done"
            else:
                # Mark last agent that ran as failed
                for ar in reversed(pipeline_result.agent_results):
                    if not ar.success:
                        st.session_state.agent_statuses[ar.agent_name] = "failed"
                        st.session_state.agent_messages[ar.agent_name] = ar.error or "Unknown error"
                        break

            # Re-render final state
            for ag in AGENTS:
                _render_agent_card(
                    agent_placeholders[ag["id"]],
                    ag,
                    st.session_state.agent_statuses[ag["id"]],
                    st.session_state.agent_messages[ag["id"]],
                )

            progress_bar.progress(1.0, text="Pipeline complete ✅")
            st.session_state.pipeline_result = pipeline_result
            st.session_state.run_count += 1

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            logger.exception("Unexpected error during pipeline: %s", exc)
            st.session_state.error_message = str(exc)
            progress_bar.empty()
        finally:
            st.session_state.running = False

# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------
if st.session_state.error_message:
    st.error(f"❌ Pipeline error: {st.session_state.error_message}")

if st.session_state.pipeline_result:
    pr = st.session_state.pipeline_result

    st.markdown("---")

    # Summary metrics
    metric_cols = st.columns(4)
    completed = sum(1 for ar in pr.agent_results if ar.success)
    metric_cols[0].metric("✅ Agents Completed", f"{completed} / {len(AGENTS)}")
    metric_cols[1].metric("⏱️ Total Time", f"{pr.total_elapsed_seconds:.1f}s")
    metric_cols[2].metric(
        "📝 Report Length",
        f"{len(pr.final_report):,} chars" if pr.final_report else "—",
    )
    metric_cols[3].metric("🔁 Runs This Session", st.session_state.run_count)

    # Per-agent expandable outputs
    st.markdown("### 📋 Agent Outputs")
    for ar in pr.agent_results:
        agent_meta = next((a for a in AGENTS if a["id"] == ar.agent_name), None)
        icon = agent_meta["icon"] if agent_meta else "🤖"
        status_str = "✅ Success" if ar.success else "❌ Failed"
        with st.expander(f"{icon} {ar.agent_name} — {status_str} ({ar.elapsed_seconds:.1f}s)"):
            if ar.success:
                st.markdown(ar.output)
            else:
                st.error(ar.error)

    # Final report
    if pr.final_report:
        st.markdown("---")
        st.markdown("### 📄 Final Report")
        with st.container():
            st.markdown(
                f'<div class="report-box">{pr.final_report}</div>',
                unsafe_allow_html=True,
            )
        st.download_button(
            label="⬇️ Download Report (Markdown)",
            data=pr.final_report,
            file_name="neuroagent_report.md",
            mime="text/markdown",
        )
