"""Research Agent – gathers background knowledge on a topic."""

from crewai import Agent, LLM

from src.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_ITERATIONS, VERBOSE_AGENTS
from utils.logger import get_logger

logger = get_logger(__name__)


def build_research_agent() -> Agent:
    """Construct and return the Research Agent."""
    logger.debug("Building Research Agent")

    llm = LLM(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE,
        api_key=OPENAI_API_KEY,
    )

    return Agent(
        role="Research Specialist",
        goal=(
            "Conduct thorough research on the given topic. "
            "Gather accurate, up-to-date information from reliable sources."
        ),
        backstory=(
            "You are an expert researcher with a PhD-level background in multiple disciplines. "
            "You excel at finding relevant information, evaluating source credibility, and "
            "synthesising complex data into clear, structured summaries."
        ),
        llm=llm,
        max_iter=MAX_ITERATIONS,
        verbose=VERBOSE_AGENTS,
        allow_delegation=False,
    )
