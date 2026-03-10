"""NeuroAgent – global configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# LLM settings
# ---------------------------------------------------------------------------
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.3"))

# ---------------------------------------------------------------------------
# Agent behaviour
# ---------------------------------------------------------------------------
MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
VERBOSE_AGENTS: bool = os.getenv("VERBOSE_AGENTS", "false").lower() == "true"
