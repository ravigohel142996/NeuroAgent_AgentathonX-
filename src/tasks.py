"""Task definitions for every agent in the NeuroAgent pipeline."""

from crewai import Task


def create_planning_task(agent, user_task: str) -> Task:
    return Task(
        description=(
            f"The user has requested the following:\n\n{user_task}\n\n"
            "Create a detailed, numbered action plan that breaks this request into clear steps. "
            "For each step specify: what needs to be done, why it matters, and what the success "
            "criteria look like. The plan should guide the remaining agents."
        ),
        expected_output=(
            "A numbered action plan (minimum 5 steps) covering research, implementation, "
            "analysis, and reporting milestones."
        ),
        agent=agent,
    )


def create_research_task(agent, user_task: str, planning_context: str = "") -> Task:
    return Task(
        description=(
            f"User task: {user_task}\n\n"
            f"Action plan from Planner:\n{planning_context}\n\n"
            "Conduct comprehensive research on all aspects of this task. "
            "Cover background theory, current best practices, relevant tools/frameworks, "
            "real-world examples, and any pitfalls to avoid."
        ),
        expected_output=(
            "A structured research summary with sections: Overview, Key Concepts, "
            "Current State of the Art, Best Practices, Tools & Resources, and Potential Challenges."
        ),
        agent=agent,
    )


def create_coding_task(agent, user_task: str, research_context: str = "") -> Task:
    return Task(
        description=(
            f"User task: {user_task}\n\n"
            f"Research findings:\n{research_context}\n\n"
            "Based on the research and the user's task, write complete, production-ready code. "
            "Include: proper error handling, logging, docstrings, type hints, and usage examples. "
            "If the task does not require code, provide relevant configuration files, scripts, "
            "or architectural diagrams instead."
        ),
        expected_output=(
            "Production-quality code with docstrings, type hints, error handling, "
            "and at least one usage example or test snippet."
        ),
        agent=agent,
    )


def create_analysis_task(agent, user_task: str, prior_context: str = "") -> Task:
    return Task(
        description=(
            f"User task: {user_task}\n\n"
            f"Prior work (plan, research, code):\n{prior_context}\n\n"
            "Perform a critical analysis of everything produced so far. "
            "Identify: strengths, weaknesses, risks, opportunities, gaps, "
            "and suggest concrete improvements."
        ),
        expected_output=(
            "An analytical report with sections: Strengths, Weaknesses, Risks, "
            "Opportunities, Key Gaps, and Recommendations."
        ),
        agent=agent,
    )


def create_report_task(agent, user_task: str, full_context: str = "") -> Task:
    return Task(
        description=(
            f"User task: {user_task}\n\n"
            f"All prior agent outputs:\n{full_context}\n\n"
            "Compile a comprehensive final report in Markdown. "
            "The report must include:\n"
            "1. Executive Summary\n"
            "2. Action Plan\n"
            "3. Research Findings\n"
            "4. Code / Implementation\n"
            "5. Analysis & Insights\n"
            "6. Recommendations & Next Steps\n"
            "7. Conclusion\n"
            "Ensure the report is professional, coherent, and ready for stakeholder delivery."
        ),
        expected_output=(
            "A complete Markdown report with all required sections, professional language, "
            "and actionable conclusions."
        ),
        agent=agent,
    )
