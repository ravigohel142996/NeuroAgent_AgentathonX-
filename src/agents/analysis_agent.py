"""Analysis Agent – evaluates information and extracts insights."""

from crewai import Agent
from langchain_openai import ChatOpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_ITERATIONS, VERBOSE_AGENTS
from utils.logger import get_logger

logger = get_logger(__name__)


def build_analysis_agent() -> Agent:
    """Construct and return the Analysis Agent."""
    logger.debug("Building Analysis Agent")

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
    )

    return Agent(
        role="Data & Strategy Analyst",
        goal=(
            "Critically evaluate research findings, code, and plans. "
            "Identify risks, gaps, opportunities, and provide actionable insights."
        ),
        backstory=(
            "You are an analytical powerhouse combining expertise in data science, business strategy, "
            "and critical thinking. You have a talent for spotting patterns, logical inconsistencies, "
            "and hidden opportunities that others miss. "
            "Your analyses are always balanced, evidence-based, and structured clearly."
        ),
        llm=llm,
        max_iter=MAX_ITERATIONS,
        verbose=VERBOSE_AGENTS,
        allow_delegation=False,
    )
