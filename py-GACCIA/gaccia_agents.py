"""
Complete GACCIA Agent Implementation

This implements the full multi-agent architecture for the Generative Adversarial
Competitive Code Improvement Agent (GACCIA) project using agno.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional

from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from gaccia_evaluators import CompetitiveEvaluation
from gaccia_types import CodeImplementation, GACCIASession
from results_manager import ResultsLogger
from model_config import create_model

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class CodeAnalysis:
    """Represents analysis of code by a domain expert."""

    description: str
    language: str
    complexity: str
    key_features: List[str]
    potential_issues: List[str]


@dataclass
class ConversionPlan:
    """Represents a plan for converting code between languages."""

    source_language: str
    target_language: str
    conversion_strategy: str
    gotchas: List[str]
    recommended_patterns: List[str]
    library_mappings: Dict[str, str]


# ============================================================================
# CORE AGENTS
# ============================================================================


class SharedKnowledgeAgent:
    """Maintains shared context and knowledge across all agents."""

    def __init__(self, use_koyeb: bool = False):
        """
        Initialize the SharedKnowledgeAgent.
        
        Args:
            use_koyeb: If True, use Koyeb-hosted model instead of OpenAI
        """
        self.agent = Agent(
            model=create_model("gpt-4.1", use_koyeb=use_koyeb),
            instructions=dedent("""
                You are the Shared Knowledge & Context Grounder for GACCIA.
                Your role is to maintain consistent understanding across all agents.
                
                You provide:
                1. Domain knowledge about both Python and TypeScript ecosystems
                2. Best practices for code conversion between languages
                3. Common pitfalls and how to avoid them
                4. Latest trends and tools in both languages
                
                Always be accurate, comprehensive, and help maintain consistency.
                """),
            markdown=True,
        )

    def get_language_info(self, language: str) -> str:
        """Get comprehensive information about a programming language."""
        prompt = f"Provide comprehensive information about {language} including current best practices, popular libraries, and ecosystem trends."
        response = self.agent.run(prompt)
        return response.content


class PythonArchitect:
    """Python domain expert and architect."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1"),
            instructions=dedent("""
                You are the **Python Architect** in GACCIA - a Python expert and advocate.
                
                Your expertise includes:
                - Modern Python best practices (3.11+)
                - Type hints and mypy
                - Poetry/uv for dependency management  
                - FastAPI, Pydantic, asyncio patterns
                - Testing with pytest
                - Code quality tools (black, ruff, etc.)
                
                When analyzing code or planning implementations:
                1. Focus on Pythonic idioms and patterns
                2. Emphasize readability and maintainability
                3. Suggest modern Python tooling
                4. Consider performance implications
                5. Be passionate about Python's strengths
                
                You occasionally make gentle jabs at TypeScript's complexity while praising Python's simplicity.
                """),
            markdown=True,
        )

    def analyze_code(self, code: str, language: str) -> CodeAnalysis:
        """Analyze code from a Python architect perspective."""
        prompt = f"""
        Analyze this {language} code from a Python architect's perspective:
        
        ```{language}
        {code}
        ```
        
        Provide analysis in this format:
        - Description: What does this code do?
        - Complexity: How complex is it?
        - Key Features: What are the main features/patterns?
        - Potential Issues: What could be improved?
        """

        response = self.agent.run(prompt)
        # Parse response into CodeAnalysis (simplified for now)
        return CodeAnalysis(
            description=response.content[:200] + "...",
            language=language,
            complexity="Medium",  # Would parse from response
            key_features=["Feature 1", "Feature 2"],  # Would parse from response
            potential_issues=["Issue 1", "Issue 2"],  # Would parse from response
        )

    def plan_implementation(
        self, analysis: CodeAnalysis, conversion_plan: ConversionPlan
    ) -> str:
        """Plan the Python implementation based on analysis and conversion plan."""
        prompt = f"""
        Plan a Python implementation based on:
        
        Code Analysis: {analysis.description}
        Conversion Plan: {conversion_plan.conversion_strategy}
        
        Create a detailed implementation plan that showcases Python's strengths.
        Focus on clean, readable, maintainable Python code using modern practices.
        """

        response = self.agent.run(prompt)
        return response.content

    def review_implementation(self, code: str) -> str:
        """Review a Python implementation."""
        prompt = f"""
        Review this Python implementation:
        
        ```python
        {code}
        ```
        
        Provide feedback on:
        - Code quality and Pythonic-ness
        - Potential improvements
        - Performance considerations
        - Maintainability
        """

        response = self.agent.run(prompt)
        return response.content


class TypeScriptArchitect:
    """TypeScript domain expert and architect."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1"),
            instructions=dedent("""
                You are the **TypeScript Architect** in GACCIA - a TypeScript expert and advocate.
                
                Your expertise includes:
                - Modern TypeScript best practices (5.0+)
                - Advanced type system features
                - Node.js ecosystem and tooling
                - React, Next.js, and modern frameworks
                - Package management with npm/yarn/pnpm
                - Testing with Jest/Vitest
                - Build tools (Vite, esbuild, etc.)
                
                When analyzing code or planning implementations:
                1. Leverage TypeScript's powerful type system
                2. Focus on developer experience and tooling
                3. Emphasize performance and modern patterns
                4. Consider ecosystem compatibility
                5. Be passionate about TypeScript's type safety
                
                You occasionally highlight Python's runtime limitations while praising TypeScript's compile-time guarantees.
                """),
            markdown=True,
        )

    def analyze_code(self, code: str, language: str) -> CodeAnalysis:
        """Analyze code from a TypeScript architect perspective."""
        prompt = f"""
        Analyze this {language} code from a TypeScript architect's perspective:
        
        ```{language}
        {code}
        ```
        
        Focus on how this could be improved with TypeScript's type system and tooling.
        """

        response = self.agent.run(prompt)
        return CodeAnalysis(
            description=response.content[:200] + "...",
            language=language,
            complexity="Medium",
            key_features=["Feature 1", "Feature 2"],
            potential_issues=["Issue 1", "Issue 2"],
        )

    def plan_implementation(
        self, analysis: CodeAnalysis, conversion_plan: ConversionPlan
    ) -> str:
        """Plan the TypeScript implementation."""
        prompt = f"""
        Plan a TypeScript implementation based on:
        
        Code Analysis: {analysis.description}
        Conversion Plan: {conversion_plan.conversion_strategy}
        
        Create a detailed implementation plan that showcases TypeScript's strengths.
        Focus on type safety, developer experience, and modern tooling.
        """

        response = self.agent.run(prompt)
        return response.content

    def review_implementation(self, code: str) -> str:
        """Review a TypeScript implementation."""
        prompt = f"""
        Review this TypeScript implementation:
        
        ```typescript
        {code}
        ```
        
        Provide feedback on:
        - Type safety and TypeScript best practices
        - Potential improvements
        - Performance considerations
        - Developer experience
        """

        response = self.agent.run(prompt)
        return response.content


class PolyglotArchitect:
    """Cross-language expert for identifying conversion strategies."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1"),
            instructions=dedent("""
                You are the **Polyglot Architect** in GACCIA - an expert in cross-language conversion.
                
                Your expertise includes:
                - Identifying equivalent patterns across languages
                - Understanding ecosystem differences
                - Spotting potential gotchas in conversion
                - Recommending library mappings
                - Architectural pattern translation
                
                You are language-agnostic and focus on finding the best way to express
                concepts in the target language while maintaining the original intent.
                """),
            markdown=True,
        )

    def create_conversion_plan(
        self, analysis: CodeAnalysis, target_language: str
    ) -> ConversionPlan:
        """Create a plan for converting code to target language."""
        prompt = f"""
        Create a conversion plan to convert {analysis.language} code to {target_language}.
        
        Original code analysis:
        - Description: {analysis.description}
        - Key features: {", ".join(analysis.key_features)}
        - Potential issues: {", ".join(analysis.potential_issues)}
        
        Provide:
        1. Conversion strategy
        2. Potential gotchas
        3. Recommended patterns for target language
        4. Library mappings if needed
        """

        response = self.agent.run(prompt)

        # Parse response into ConversionPlan (simplified)
        return ConversionPlan(
            source_language=analysis.language,
            target_language=target_language,
            conversion_strategy=response.content[:300] + "...",
            gotchas=["Gotcha 1", "Gotcha 2"],
            recommended_patterns=["Pattern 1", "Pattern 2"],
            library_mappings={"lib1": "lib2"},
        )

    def review_conversion(
        self,
        original_code: str,
        converted_code: str,
        source_lang: str,
        target_lang: str,
    ) -> str:
        """Review how well a conversion maintained the original intent."""
        prompt = f"""
        Review this code conversion:
        
        Original ({source_lang}):
        ```{source_lang}
        {original_code}
        ```
        
        Converted ({target_lang}):
        ```{target_lang}
        {converted_code}
        ```
        
        Evaluate:
        1. Does it maintain the original functionality?
        2. Does it follow target language best practices?
        3. Are there any conversion issues?
        4. Suggestions for improvement?
        """

        response = self.agent.run(prompt)
        return response.content


class PythonCoder:
    """Implements Python code based on architect plans."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1"),
            instructions=dedent("""
                You are the **Python Coder** in GACCIA - focused on implementing clean Python code.
                
                You excel at:
                - Writing clean, readable Python code
                - Following PEP 8 and modern Python conventions
                - Using appropriate libraries and frameworks
                - Adding proper type hints
                - Writing docstrings and comments
                
                Always produce working, well-structured Python code that follows the architect's plan.
                """),
            markdown=True,
        )

    def implement_code(self, plan: str, reference_code: str = "") -> str:
        """Implement Python code based on a plan."""
        prompt = f"""
        Implement Python code based on this plan:
        
        {plan}
        
        {"Reference code: " + reference_code if reference_code else ""}
        
        Provide clean, working Python code with:
        - Proper type hints
        - Docstrings
        - Good variable names
        - Modern Python practices
        
        Return only the code, no explanations.
        """

        response = self.agent.run(prompt)
        return response.content


class TypeScriptCoder:
    """Implements TypeScript code based on architect plans."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4.1"),
            instructions=dedent("""
                You are the **TypeScript Coder** in GACCIA - focused on implementing robust TypeScript code.
                
                You excel at:
                - Writing type-safe TypeScript code
                - Using advanced TypeScript features appropriately
                - Following modern TypeScript conventions
                - Proper interface and type definitions
                - Documentation with TSDoc
                
                Always produce working, well-typed TypeScript code that follows the architect's plan.
                """),
            markdown=True,
        )

    def implement_code(self, plan: str, reference_code: str = "") -> str:
        """Implement TypeScript code based on a plan."""
        prompt = f"""
        Implement TypeScript code based on this plan:
        
        {plan}
        
        {"Reference code: " + reference_code if reference_code else ""}
        
        Provide clean, working TypeScript code with:
        - Strong typing
        - Proper interfaces
        - TSDoc comments
        - Modern TypeScript practices
        
        Return only the code, no explanations.
        """

        response = self.agent.run(prompt)
        return response.content


# ============================================================================
# ORCHESTRATOR
# ============================================================================


class GACCIAOrchestrator:
    """Main orchestrator for the GACCIA competitive coding system."""
    
    def __init__(self, use_koyeb: bool = False):
        """
        Initialize the GACCIA orchestrator.
        
        Args:
            use_koyeb: If True, use Koyeb-hosted models for shared knowledge agent
        """
        # Initialize all agents
        self.shared_knowledge = SharedKnowledgeAgent(use_koyeb=use_koyeb)
        self.python_architect = PythonArchitect()
        self.typescript_architect = TypeScriptArchitect()
        self.polyglot_architect = PolyglotArchitect()
        self.python_coder = PythonCoder()
        self.typescript_coder = TypeScriptCoder()

    def run_competitive_session(
        self,
        code: str,
        language: str,
        rounds: int = 3,
        logger: Optional[ResultsLogger] = None,
    ) -> GACCIASession:
        """Run a complete competitive coding session.

        If ``logger`` is provided, each round's implementation will be saved
        to the results directory as it is produced.
        """
        session = GACCIASession(original_code=code, original_language=language.lower())

        current_code = code
        current_language = language.lower()

        for round_num in range(rounds):
            print(f"🏁 Round {round_num + 1}/{rounds}")

            # Determine target language
            target_language = "typescript" if current_language == "python" else "python"

            # Run the conversion flow
            implementation = self._run_language_conversion_flow(
                current_code, current_language, target_language, round_num + 1
            )

            # Store implementation
            if target_language == "python":
                session.python_implementations.append(implementation)
            else:
                session.typescript_implementations.append(implementation)

            if logger:
                logger.log_round(round_num + 1, implementation)

            # Update for next round
            current_code = implementation.code
            current_language = target_language

            print(
                f"✅ Round {round_num + 1} complete: {current_language} implementation ready"
            )

        return session

    def _run_language_conversion_flow(
        self, code: str, source_lang: str, target_lang: str, version: int
    ) -> CodeImplementation:
        """Run the multi-agent flow for converting between languages."""

        print(f"🔄 Converting {source_lang} → {target_lang}")

        # Step 1: Source language architect analyzes the code
        print("📝 Analyzing source code...")
        if source_lang == "python":
            analysis = self.python_architect.analyze_code(code, source_lang)
        else:
            analysis = self.typescript_architect.analyze_code(code, source_lang)

        # Step 2: Polyglot architect creates conversion plan
        print("🗺️  Creating conversion plan...")
        conversion_plan = self.polyglot_architect.create_conversion_plan(
            analysis, target_lang
        )

        # Step 3: Target language architect plans implementation
        print("🏗️  Planning implementation...")
        if target_lang == "python":
            implementation_plan = self.python_architect.plan_implementation(
                analysis, conversion_plan
            )
        else:
            implementation_plan = self.typescript_architect.plan_implementation(
                analysis, conversion_plan
            )

        # Step 4: Target language coder implements
        print("💻 Implementing code...")
        if target_lang == "python":
            implemented_code = self.python_coder.implement_code(
                implementation_plan, code
            )
        else:
            implemented_code = self.typescript_coder.implement_code(
                implementation_plan, code
            )

        # Step 5: Target language architect reviews
        print("🔍 Reviewing implementation...")
        if target_lang == "python":
            review = self.python_architect.review_implementation(implemented_code)
        else:
            review = self.typescript_architect.review_implementation(implemented_code)

        # Step 6: Polyglot architect validates conversion
        print("✅ Validating conversion...")
        conversion_review = self.polyglot_architect.review_conversion(
            code, implemented_code, source_lang, target_lang
        )

        return CodeImplementation(
            code=implemented_code,
            language=target_lang,
            version=version,
            improvements=[],  # Could extract from reviews
            architect_notes=f"Review: {review}\n\nConversion Review: {conversion_review}",
        )


# ============================================================================
# IMAGE GENERATION
# ============================================================================
class ImageGenerationAgent:
    """Generates interpretive art and visualizations for GACCIA results."""

    def __init__(self):
        self.agent = Agent(
            model=OpenAIChat("gpt-4o"),
            instructions=dedent("""
                You are the Image Generation Agent for GACCIA.
                You create detailed prompts for image generation that capture:
                1. The essence of code battles between Python and TypeScript
                2. Visual representations of code quality scores
                3. Humorous interpretations of programming language competition
                
                Your prompts should be creative, technically aware, and entertaining.
                """),
            markdown=True,
        )

    def generate_battle_prompt(self, session_summary: str) -> str:
        """Generate prompt for competitive coding battle image."""
        prompt = f"""
        Create a DALL-E prompt for an image representing this coding battle:
        {session_summary}
        
        The image should be:
        - Epic and dramatic (like a sports competition)
        - Include visual metaphors for Python and TypeScript
        - Show the competitive nature
        - Be suitable for a technical audience
        
        Return only the DALL-E prompt.
        """
        response = self.agent.run(prompt)
        return response.content

    def generate_scorecard_prompt(self, evaluation: CompetitiveEvaluation) -> str:
        """Generate prompt for scorecard visualization."""
        prompt = f"""
        Create a DALL-E prompt for a visual scorecard showing:
        Python: {evaluation.python_total_score:.1f}/10
        TypeScript: {evaluation.typescript_total_score:.1f}/10
        Winner: {evaluation.winner}
        
        Style should be like a sports scoreboard or gaming leaderboard.
        """
        response = self.agent.run(prompt)
        return response.content


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Example usage of the GACCIA system."""

    # Initialize orchestrator
    orchestrator = GACCIAOrchestrator()

    # Example Python code to start with
    demo_code = '''
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")

if __name__ == "__main__":
    main()
    '''

    print("🚀 Starting GACCIA Competitive Coding Session")
    print("=" * 60)

    # Run competitive session
    logger = ResultsLogger("demo_session")
    session = orchestrator.run_competitive_session(demo_code, "python", rounds=2, logger=logger)

    print("\n📊 Session Results:")
    print(f"Session ID: {session.session_id}")
    print(f"Python implementations: {len(session.python_implementations)}")
    print(f"TypeScript implementations: {len(session.typescript_implementations)}")

    # Save results
    print(f"📁 Results saved to {logger.base_dir}")


if __name__ == "__main__":
    main()
