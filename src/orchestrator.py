"""Orchestrator – drives the multi-agent pipeline and streams progress."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from crewai import Crew, Process

from src.agents import (
    build_analysis_agent,
    build_coding_agent,
    build_planner_agent,
    build_report_agent,
    build_research_agent,
)
from src.tasks import (
    create_analysis_task,
    create_coding_task,
    create_planning_task,
    create_report_task,
    create_research_task,
)
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class AgentResult:
    agent_name: str
    output: str
    elapsed_seconds: float
    success: bool
    error: Optional[str] = None


@dataclass
class PipelineResult:
    user_task: str
    agent_results: list[AgentResult] = field(default_factory=list)
    final_report: str = ""
    total_elapsed_seconds: float = 0.0
    success: bool = False
    error: Optional[str] = None


# Type alias for the progress callback
ProgressCallback = Callable[[str, str], None]  # (agent_name, status_message)


class Orchestrator:
    """Runs the 5-agent pipeline sequentially and reports progress via a callback."""

    AGENT_SEQUENCE = [
        ("Planner", "Breaking the task into an action plan…"),
        ("Researcher", "Gathering research and background knowledge…"),
        ("Coder", "Writing production-ready code…"),
        ("Analyst", "Analysing findings and identifying insights…"),
        ("Reporter", "Compiling the final structured report…"),
    ]

    def __init__(self, progress_callback: Optional[ProgressCallback] = None) -> None:
        self._cb = progress_callback or (lambda name, msg: None)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self, user_task: str) -> PipelineResult:
        """Execute the full multi-agent pipeline for *user_task*."""
        logger.info("Pipeline started | task=%r", user_task)
        pipeline_start = time.perf_counter()
        result = PipelineResult(user_task=user_task)

        try:
            # Build agents
            planner = build_planner_agent()
            researcher = build_research_agent()
            coder = build_coding_agent()
            analyst = build_analysis_agent()
            reporter = build_report_agent()

            # -----------------------------------------------------------
            # Step 1 – Planning
            # -----------------------------------------------------------
            plan_output = self._run_agent_step(
                name="Planner",
                status="Breaking the task into an action plan…",
                agent=planner,
                task_factory=lambda: create_planning_task(planner, user_task),
                result=result,
            )

            # -----------------------------------------------------------
            # Step 2 – Research
            # -----------------------------------------------------------
            research_output = self._run_agent_step(
                name="Researcher",
                status="Gathering research and background knowledge…",
                agent=researcher,
                task_factory=lambda: create_research_task(researcher, user_task, plan_output),
                result=result,
            )

            # -----------------------------------------------------------
            # Step 3 – Coding
            # -----------------------------------------------------------
            code_output = self._run_agent_step(
                name="Coder",
                status="Writing production-ready code…",
                agent=coder,
                task_factory=lambda: create_coding_task(coder, user_task, research_output),
                result=result,
            )

            # -----------------------------------------------------------
            # Step 4 – Analysis
            # -----------------------------------------------------------
            prior = f"Plan:\n{plan_output}\n\nResearch:\n{research_output}\n\nCode:\n{code_output}"
            analysis_output = self._run_agent_step(
                name="Analyst",
                status="Analysing findings and identifying insights…",
                agent=analyst,
                task_factory=lambda: create_analysis_task(analyst, user_task, prior),
                result=result,
            )

            # -----------------------------------------------------------
            # Step 5 – Report
            # -----------------------------------------------------------
            full_context = (
                f"Plan:\n{plan_output}\n\n"
                f"Research:\n{research_output}\n\n"
                f"Code:\n{code_output}\n\n"
                f"Analysis:\n{analysis_output}"
            )
            report_output = self._run_agent_step(
                name="Reporter",
                status="Compiling the final structured report…",
                agent=reporter,
                task_factory=lambda: create_report_task(reporter, user_task, full_context),
                result=result,
            )

            result.final_report = report_output
            result.success = True
            logger.info("Pipeline completed successfully")

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            logger.exception("Pipeline failed: %s", exc)
            result.error = str(exc)
            result.success = False

        result.total_elapsed_seconds = time.perf_counter() - pipeline_start
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_agent_step(
        self,
        *,
        name: str,
        status: str,
        agent,
        task_factory: Callable,
        result: PipelineResult,
    ) -> str:
        """Run a single agent, update the pipeline result, and return its output."""
        self._cb(name, status)
        logger.info("Agent starting | agent=%s", name)
        start = time.perf_counter()

        try:
            task = task_factory()
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False,
            )
            crew_result = crew.kickoff()
            # crew.kickoff() returns a CrewOutput object; .raw is the string output
            output: str = getattr(crew_result, "raw", str(crew_result))
            elapsed = time.perf_counter() - start
            logger.info("Agent finished | agent=%s | elapsed=%.1fs", name, elapsed)
            self._cb(name, f"✅ Done ({elapsed:.1f}s)")
            result.agent_results.append(
                AgentResult(agent_name=name, output=output, elapsed_seconds=elapsed, success=True)
            )
            return output

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("Agent failed | agent=%s | error=%s", name, exc, exc_info=True)
            self._cb(name, f"❌ Failed: {exc}")
            result.agent_results.append(
                AgentResult(
                    agent_name=name,
                    output="",
                    elapsed_seconds=elapsed,
                    success=False,
                    error=str(exc),
                )
            )
            raise
