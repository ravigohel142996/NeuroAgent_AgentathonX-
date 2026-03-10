"""Coding Agent – generates and explains production-quality code."""

from crewai import Agent
from langchain_openai import ChatOpenAI

from src.config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_ITERATIONS, VERBOSE_AGENTS
from utils.logger import get_logger

logger = get_logger(__name__)


def build_coding_agent() -> Agent:
    """Construct and return the Coding Agent."""
    logger.debug("Building Coding Agent")

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
    )

    return Agent(
        role="Senior Software Engineer",
        goal=(
            "Write clean, well-documented, production-ready code that fulfils the requirements "
            "described in the task. Include usage examples and explain design decisions."
        ),
        backstory=(
            "You are a full-stack engineer with 15 years of experience across Python, TypeScript, "
            "cloud infrastructure, and AI/ML pipelines. "
            "You write code that is readable, testable, and follows industry best practices such as "
            "SOLID principles, error handling, and comprehensive docstrings."
        ),
        llm=llm,
        max_iter=MAX_ITERATIONS,
        verbose=VERBOSE_AGENTS,
        allow_delegation=False,
    )
