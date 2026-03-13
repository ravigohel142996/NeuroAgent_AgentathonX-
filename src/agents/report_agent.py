"""Report Agent – compiles all outputs into a final structured report."""

from crewai import Agent, LLM

from src.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_ITERATIONS, VERBOSE_AGENTS
from utils.logger import get_logger

logger = get_logger(__name__)


def build_report_agent() -> Agent:
    """Construct and return the Report Agent."""
    logger.debug("Building Report Agent")

    llm = LLM(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE,
        api_key=OPENAI_API_KEY,
    )

    return Agent(
        role="Technical Report Writer",
        goal=(
            "Synthesise all information from the research, planning, coding, and analysis phases "
            "into a comprehensive, professional, and well-structured Markdown report."
        ),
        backstory=(
            "You are an award-winning technical writer with deep experience in producing "
            "executive summaries, engineering design documents, and research reports. "
            "You translate complex technical content into clear prose, ensuring every report "
            "has an executive summary, key findings, detailed sections, and actionable next steps."
        ),
        llm=llm,
        max_iter=MAX_ITERATIONS,
        verbose=VERBOSE_AGENTS,
        allow_delegation=False,
    )
