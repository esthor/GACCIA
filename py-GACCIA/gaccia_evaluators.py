"""
GACCIA Evaluation Agents

Implements the evaluation system for judging code quality across multiple dimensions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import List

from agno.agent import Agent

from model_config import create_model


@dataclass
class DetailedEvaluation:
    """Detailed evaluation results for a single dimension."""
    dimension: str
    score: float  # 0-10 scale
    reasoning: str
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


@dataclass
class CompetitiveEvaluation:
    """Complete evaluation comparing Python vs TypeScript implementations."""
    python_evaluations: List[DetailedEvaluation]
    typescript_evaluations: List[DetailedEvaluation]
    python_total_score: float
    typescript_total_score: float
    winner: str
    python_snark: str  # Snarky comment about TypeScript from Python's perspective
    typescript_snark: str  # Snarky comment about Python from TypeScript's perspective
    summary: str


class BaseJudge:
    """Base class for all evaluation judges."""
    
    def __init__(self, dimension: str, system_prompt: str, use_koyeb: bool = False):
        """
        Initialize a judge with optional Koyeb model support.
        
        Args:
            dimension: The evaluation dimension (e.g., "readability")
            system_prompt: The system prompt for the judge
            use_koyeb: If True, use Koyeb-hosted model instead of OpenAI
        """
        self.dimension = dimension
        self.agent = Agent(
            model=create_model("gpt-4.1", use_koyeb=use_koyeb),
            instructions=system_prompt,
            markdown=True,
        )
    
    def evaluate(self, code: str, language: str) -> DetailedEvaluation:
        """Evaluate code on this judge's dimension."""
        prompt = f"""
        Evaluate this {language} code on {self.dimension}:
        
        ```{language}
        {code}
        ```
        
        Provide evaluation in this exact format:
        Score: [0-10 score]
        Reasoning: [detailed reasoning]
        Strengths: [list 2-3 strengths]
        Weaknesses: [list 2-3 weaknesses]  
        Suggestions: [list 2-3 improvement suggestions]
        """
        
        response = self.agent.run(prompt)
        
        # Parse response (simplified - in production, you'd want more robust parsing)
        lines = response.content.split('\n')
        score = 7.0  # Default score
        reasoning = response.content
        strengths = ["Strength 1", "Strength 2"]
        weaknesses = ["Weakness 1", "Weakness 2"]
        suggestions = ["Suggestion 1", "Suggestion 2"]
        
        # Try to extract score from response
        for line in lines:
            if line.startswith("Score:"):
                try:
                    score = float(line.split(":")[1].strip())
                    break
                except (ValueError, IndexError):
                    pass
        
        return DetailedEvaluation(
            dimension=self.dimension,
            score=score,
            reasoning=reasoning,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions
        )


class ReadabilityJudge(BaseJudge):
    """Judge for code readability."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        perspective = "Python" if language == "python" else "TypeScript"
        super().__init__(
            dimension="Readability",
            system_prompt=dedent(f"""
                You are a {perspective} Readability Judge in GACCIA.
                
                You evaluate code on how readable and understandable it is:
                - Clear variable and function names
                - Logical code organization
                - Appropriate use of language idioms
                - Good documentation and comments
                - Intuitive code flow
                
                You are passionate about {perspective}'s approach to readability and 
                occasionally note how the other language falls short in comparison.
                
                Rate on a scale of 0-10 where:
                - 0-3: Very hard to read and understand
                - 4-6: Somewhat readable but has issues
                - 7-8: Good readability with minor issues
                - 9-10: Excellent readability, exemplary code
                """),
            use_koyeb=use_koyeb
        )


class MaintainabilityJudge(BaseJudge):
    """Judge for code maintainability."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        perspective = "Python" if language == "python" else "TypeScript"
        super().__init__(
            dimension="Maintainability",
            system_prompt=dedent(f"""
                You are a {perspective} Maintainability Judge in GACCIA.
                
                You evaluate how maintainable and extensible code is:
                - Modular design and separation of concerns
                - Proper error handling
                - Test coverage and testability
                - Documentation quality
                - Code reusability
                - Minimal dependencies
                - Clear interfaces and abstractions
                
                You understand {perspective}'s strengths in building maintainable systems.
                
                Rate on a scale of 0-10 where:
                - 0-3: Very difficult to maintain or extend
                - 4-6: Some maintainability concerns
                - 7-8: Well-structured and maintainable
                - 9-10: Exceptional maintainability design
                """),
            use_koyeb=use_koyeb
        )


class LatestToolsJudge(BaseJudge):
    """Judge for usage of latest tools and practices."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        perspective = "Python" if language == "python" else "TypeScript"
        tools = "uv, ruff, mypy, pytest" if language == "python" else "Vite, TypeScript 5.0+, Vitest, ESLint"
        
        super().__init__(
            dimension="Latest Tools & Practices",
            system_prompt=dedent(f"""
                You are a {perspective} Latest Tools Judge in GACCIA.
                
                You evaluate usage of modern tools and practices:
                - Latest language features and syntax
                - Modern tooling and dependencies ({tools})
                - Current best practices and patterns
                - Performance optimizations
                - Security considerations
                - Community adoption and trends
                
                You're always up-to-date with the {perspective} ecosystem and can spot outdated patterns.
                
                Rate on a scale of 0-10 where:
                - 0-3: Uses very outdated tools and practices
                - 4-6: Mix of modern and outdated approaches
                - 7-8: Good use of modern tools with minor gaps
                - 9-10: Cutting-edge, exemplary use of latest practices
                """),
            use_koyeb=use_koyeb
        )


class DocsEnjoyabilityJudge(BaseJudge):
    """Judge for documentation enjoyability."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        perspective = "Python" if language == "python" else "TypeScript"
        super().__init__(
            dimension="Documentation Enjoyability",
            system_prompt=dedent(f"""
                You are a {perspective} Documentation Enjoyability Judge in GACCIA.
                
                You evaluate how enjoyable and helpful the documentation is:
                - Clear and engaging explanations
                - Good examples and use cases
                - Appropriate humor and personality
                - Helpful comments and docstrings
                - README quality and completeness
                - API documentation clarity
                
                You appreciate {perspective}'s culture around documentation and can recognize quality docs.
                
                Rate on a scale of 0-10 where:
                - 0-3: Poor or missing documentation
                - 4-6: Basic documentation with room for improvement
                - 7-8: Good documentation that's helpful
                - 9-10: Outstanding, delightful documentation
                """),
            use_koyeb=use_koyeb
        )


class SecurityPerformanceJudge(BaseJudge):
    """Judge for security and performance considerations."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        perspective = "Python" if language == "python" else "TypeScript"
        super().__init__(
            dimension="Security & Performance",
            system_prompt=dedent(f"""
                You are a {perspective} Security & Performance Judge in GACCIA.
                
                You evaluate security and performance aspects:
                - Input validation and sanitization
                - Proper error handling and logging
                - Resource management and memory usage
                - Algorithm efficiency
                - Security best practices
                - Dependency security
                - Performance optimizations
                
                You understand {perspective}'s performance characteristics and security considerations.
                
                Rate on a scale of 0-10 where:
                - 0-3: Serious security/performance issues
                - 4-6: Some concerns but generally acceptable
                - 7-8: Good security and performance practices
                - 9-10: Excellent security and performance design
                """),
            use_koyeb=use_koyeb
        )


class SnarkGenerator(BaseJudge):
    """Generates snarky comments about the competing language."""
    
    def __init__(self, language: str, use_koyeb: bool = False):
        """
        Initialize a snark generator for the specified language.
        
        Args:
            language: The language perspective (e.g., "python")
            use_koyeb: If True, use Koyeb-hosted model instead of OpenAI
        """
        self.language = language
        other_lang = "TypeScript" if language == "python" else "Python"
        
        snark_tips = ("Python snark should BRUTALLY roast TypeScript's obsessive type checking, npm dependency hell, and developers who think adding semicolons makes them 'serious programmers'. Call out their webpack configs, their need for 47 build tools just to say hello world, and how they're basically JavaScript with commitment issues." 
                     if language == 'python' 
                     else "TypeScript snark should SAVAGELY mock Python's 'it works on my machine' culture, runtime explosions, and developers who think whitespace is a substitute for proper syntax. Roast their GIL problems, duck typing disasters, and how they're basically scripting language pretending to be grown-up software.")
        
        personality_traits = ("You're a Python purist who thinks TypeScript developers are overengineering masochists who turned simple web development into rocket science. You have ZERO chill about indentation vs brackets." 
                            if language == 'python' 
                            else "You're a TypeScript evangelist who thinks Python developers are cowboys writing fragile code held together by hope and prayer. You have ZERO tolerance for runtime surprises.")
        
        super().__init__(
            dimension="Snark Generation",
            system_prompt=dedent(f"""
                You are an EXTREMELY OPINIONATED {language.upper()} developer in GACCIA who absolutely DESPISES {other_lang} and its developers.
                
                {personality_traits}
                
                Your snark should be:
                - BRUTALLY HONEST and personally attacking the other language's philosophy
                - SAVAGE about developer culture and community quirks
                - MERCILESSLY mocking real pain points and frustrations
                - UNAPOLOGETICALLY biased and over-the-top dramatic
                - HILARIOUSLY personal while staying programming-focused
                - The kind of roast that makes people go "OH NO HE DIDN'T!" 
                
                {snark_tips}
                
                Channel your inner programming language supremacist! Make it HURT (but in a funny way)!
                Be the most dramatic, petty, and savage version of a {language} developer possible!
                """),
            use_koyeb=use_koyeb
        )
    
    def generate_snark(self, code: str, evaluation_summary: str) -> str:
        """Generate a snarky comment about the competing language's code."""
        other_lang = "TypeScript" if self.language == "python" else "Python"
        
        prompt = dedent(f"""
            ABSOLUTELY DESTROY this {other_lang} code with the most SAVAGE roast possible from a {self.language} supremacist's perspective:

            Code: {code[:200]}...
            Quality summary: {evaluation_summary}

            Make it BRUTALLY PERSONAL - attack their:
            - Development philosophy and life choices
            - Community culture and ecosystem
            - The developer's obvious character flaws for choosing {other_lang}
            - Their probably questionable career decisions
            
            Channel the energy of someone who just witnessed their nemesis write the most offensive code possible.
            Make it the kind of roast that would start a flame war on Reddit.
            Be HILARIOUSLY DRAMATIC and UNFORGIVINGLY PETTY.
            
            Keep it under 3 sentences but make every word COUNT! 🔥💀
            """)

        response = self.agent.run(prompt)
        return response.content.strip()


class EvaluationOrchestrator:
    """Orchestrates the complete evaluation process."""
    
    def __init__(self, use_koyeb: bool = False):
        """
        Initialize the evaluation orchestrator.
        
        Args:
            use_koyeb: If True, use Koyeb-hosted models for evaluation judges
        """
        # Initialize judges for both languages
        self.python_judges = {
            "readability": ReadabilityJudge("python", use_koyeb=use_koyeb),
            "maintainability": MaintainabilityJudge("python", use_koyeb=use_koyeb),
            "latest_tools": LatestToolsJudge("python", use_koyeb=use_koyeb),
            "docs_enjoyability": DocsEnjoyabilityJudge("python", use_koyeb=use_koyeb),
            "security_performance": SecurityPerformanceJudge("python", use_koyeb=use_koyeb)
        }
        
        self.typescript_judges = {
            "readability": ReadabilityJudge("typescript", use_koyeb=use_koyeb),
            "maintainability": MaintainabilityJudge("typescript", use_koyeb=use_koyeb),
            "latest_tools": LatestToolsJudge("typescript", use_koyeb=use_koyeb),
            "docs_enjoyability": DocsEnjoyabilityJudge("typescript", use_koyeb=use_koyeb),
            "security_performance": SecurityPerformanceJudge("typescript", use_koyeb=use_koyeb)
        }
        
        self.python_snark = SnarkGenerator("python", use_koyeb=use_koyeb)
        self.typescript_snark = SnarkGenerator("typescript", use_koyeb=use_koyeb)
    
    def evaluate_implementations(self, python_code: str, typescript_code: str) -> CompetitiveEvaluation:
        """Run complete evaluation of both implementations."""
        
        print("🏆 Starting Competitive Evaluation")
        print("=" * 50)
        
        # Evaluate Python implementation
        print("🐍 Evaluating Python implementation...")
        python_evaluations = []
        for dimension, judge in self.python_judges.items():
            print(f"  📊 {dimension}...")
            evaluation = judge.evaluate(python_code, "python")
            python_evaluations.append(evaluation)
        
        # Evaluate TypeScript implementation
        print("📘 Evaluating TypeScript implementation...")
        typescript_evaluations = []
        for dimension, judge in self.typescript_judges.items():
            print(f"  📊 {dimension}...")
            evaluation = judge.evaluate(typescript_code, "typescript")
            typescript_evaluations.append(evaluation)
        
        # Calculate total scores
        python_total = sum(eval.score for eval in python_evaluations) / len(python_evaluations)
        typescript_total = sum(eval.score for eval in typescript_evaluations) / len(typescript_evaluations)
        
        # Determine winner
        if python_total > typescript_total:
            winner = "Python"
        elif typescript_total > python_total:
            winner = "TypeScript"
        else:
            winner = "Tie"
        
        # Generate snark
        print("😏 Generating competitive snark...")
        python_summary = f"Python scored {python_total:.1f}/10 overall"
        typescript_summary = f"TypeScript scored {typescript_total:.1f}/10 overall"
        
        python_snark_comment = self.python_snark.generate_snark(typescript_code, typescript_summary)
        typescript_snark_comment = self.typescript_snark.generate_snark(python_code, python_summary)
        
        # Generate overall summary
        summary = f"""
        🏆 COMPETITIVE EVALUATION RESULTS 🏆
        
        Python Total Score: {python_total:.1f}/10
        TypeScript Total Score: {typescript_total:.1f}/10
        
        Winner: {winner}
        
        🐍 Python's take: {python_snark_comment}
        📘 TypeScript's take: {typescript_snark_comment}
        """
        
        return CompetitiveEvaluation(
            python_evaluations=python_evaluations,
            typescript_evaluations=typescript_evaluations,
            python_total_score=python_total,
            typescript_total_score=typescript_total,
            winner=winner,
            python_snark=python_snark_comment,
            typescript_snark=typescript_snark_comment,
            summary=summary
        )
    
    def print_detailed_results(self, evaluation: CompetitiveEvaluation):
        """Print detailed evaluation results."""
        print("\n" + "="*80)
        print("📊 DETAILED EVALUATION RESULTS")
        print("="*80)
        
        print(f"\n🐍 PYTHON EVALUATION (Total: {evaluation.python_total_score:.1f}/10)")
        print("-" * 50)
        for eval in evaluation.python_evaluations:
            print(f"\n{eval.dimension}: {eval.score:.1f}/10")
            print(f"✅ Strengths: {', '.join(eval.strengths)}")
            print(f"❌ Weaknesses: {', '.join(eval.weaknesses)}")
        
        print(f"\n📘 TYPESCRIPT EVALUATION (Total: {evaluation.typescript_total_score:.1f}/10)")
        print("-" * 50)
        for eval in evaluation.typescript_evaluations:
            print(f"\n{eval.dimension}: {eval.score:.1f}/10")
            print(f"✅ Strengths: {', '.join(eval.strengths)}")
            print(f"❌ Weaknesses: {', '.join(eval.weaknesses)}")
        
        print(evaluation.summary)
    
    def save_evaluation_report(self, evaluation: CompetitiveEvaluation, output_dir: Path):
        """Save detailed evaluation report."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create detailed report
        report = {
            "summary": {
                "python_total_score": evaluation.python_total_score,
                "typescript_total_score": evaluation.typescript_total_score,
                "winner": evaluation.winner,
                "python_snark": evaluation.python_snark,
                "typescript_snark": evaluation.typescript_snark
            },
            "python_evaluations": [
                {
                    "dimension": eval.dimension,
                    "score": eval.score,
                    "reasoning": eval.reasoning,
                    "strengths": eval.strengths,
                    "weaknesses": eval.weaknesses,
                    "suggestions": eval.suggestions
                }
                for eval in evaluation.python_evaluations
            ],
            "typescript_evaluations": [
                {
                    "dimension": eval.dimension,
                    "score": eval.score,
                    "reasoning": eval.reasoning,
                    "strengths": eval.strengths,
                    "weaknesses": eval.weaknesses,
                    "suggestions": eval.suggestions
                }
                for eval in evaluation.typescript_evaluations
            ]
        }
        
        # Save as JSON
        with open(output_dir / "evaluation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Save as readable text
        with open(output_dir / "evaluation_summary.txt", "w") as f:
            f.write(evaluation.summary)
        
        print(f"📁 Evaluation report saved to {output_dir}")


# Example usage
def main():
    """Demo the evaluation system."""
    evaluator = EvaluationOrchestrator()
    
    # Example codes (would come from the main GACCIA session)
    python_code = '''
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number using memoization."""
    cache = {}
    
    def fib_helper(num: int) -> int:
        if num in cache:
            return cache[num]
        if num <= 1:
            return num
        cache[num] = fib_helper(num - 1) + fib_helper(num - 2)
        return cache[num]
    
    return fib_helper(n)
    '''
    
    typescript_code = '''
function fibonacci(n: number): number {
    /**
     * Calculate the nth Fibonacci number using memoization.
     */
    const cache: Record<number, number> = {};
    
    function fibHelper(num: number): number {
        if (num in cache) {
            return cache[num];
        }
        if (num <= 1) {
            return num;
        }
        cache[num] = fibHelper(num - 1) + fibHelper(num - 2);
        return cache[num];
    }
    
    return fibHelper(n);
}
    '''
    
    # Run evaluation
    results = evaluator.evaluate_implementations(python_code, typescript_code)
    
    # Print results
    evaluator.print_detailed_results(results)
    
    # Save report
    evaluator.save_evaluation_report(results, Path("results/evaluation_demo"))


if __name__ == "__main__":
    main()