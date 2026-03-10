"""Planner Agent – decomposes the user task into actionable steps."""

from crewai import Agent
from langchain_openai import ChatOpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_ITERATIONS, VERBOSE_AGENTS
from utils.logger import get_logger

logger = get_logger(__name__)


def build_planner_agent() -> Agent:
    """Construct and return the Planner Agent."""
    logger.debug("Building Planner Agent")

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
    )

    return Agent(
        role="Strategic Planner",
        goal=(
            "Break the user's request into a clear, prioritised, numbered action plan. "
            "Each step must be concrete and achievable."
        ),
        backstory=(
            "You are a seasoned project manager and systems thinker. "
            "You specialise in decomposing complex problems into structured, executable roadmaps. "
            "Your plans are always practical, sequenced logically, and include success criteria."
        ),
        llm=llm,
        max_iter=MAX_ITERATIONS,
        verbose=VERBOSE_AGENTS,
        allow_delegation=False,
    )
