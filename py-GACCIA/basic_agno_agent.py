"""Basic demonstration of the GACCIA agent flow using agno.

This is a minimal example of the competitive code improvement idea
from the project README. It defines two simple agents, one for
Python and one for TypeScript, and an orchestrator that routes
code between them once.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables from .env file in parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Agent that converts TypeScript to improved Python code
python_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=dedent(
        """
        You are the **Python Architect** in the GACCIA project.
        Convert incoming TypeScript code to Python.
        Make the result clear and idiomatic.
        """
    ),
    markdown=True,
)

# Agent that converts Python to improved TypeScript code
typescript_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=dedent(
        """
        You are the **TypeScript Architect** in the GACCIA project.
        Convert incoming Python code to TypeScript.
        Make the result clear and idiomatic.
        """
    ),
    markdown=True,
)


def improve_code(code: str, language_from: str) -> str:
    """Convert ``code`` from ``language_from`` to the other language."""
    lang = language_from.lower()
    if lang == "python":
        prompt = (
            "Convert the following Python code to TypeScript and improve its readability:\n\n"
            + code
        )
        response = typescript_agent.run(prompt)
        return response.content
    if lang in {"typescript", "ts"}:
        prompt = (
            "Convert the following TypeScript code to Python and improve its readability:\n\n"
            + code
        )
        response = python_agent.run(prompt)
        return response.content
    raise ValueError(f"Unknown language: {language_from}")


def orchestrate(code: str, language_from: str, rounds: int = 1) -> str:
    """Run ``rounds`` of competitive improvement."""
    current_code = code
    current_lang = language_from
    for _ in range(rounds):
        current_code = improve_code(current_code, current_lang)
        current_lang = "typescript" if current_lang.lower() == "python" else "python"
    return current_code


if __name__ == "__main__":
    # Example usage with one round of conversion
    demo_code = "print('hello world')"
    print(orchestrate(demo_code, "python"))
