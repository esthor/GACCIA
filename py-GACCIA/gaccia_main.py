"""
Complete GACCIA Integration

This brings together the core agents and evaluation system into a complete
competitive coding improvement platform.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from results_manager import ResultsLogger

from dotenv import load_dotenv

# Import our GACCIA modules (assuming they're in the same directory)
from gaccia_agents import GACCIAOrchestrator, GACCIASession, CodeImplementation
from gaccia_evaluators import EvaluationOrchestrator, CompetitiveEvaluation
from model_config import get_model_config_info

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class CompletedGACCIASession:
    """A complete GACCIA session with implementations and evaluations."""
    
    def __init__(self, session: GACCIASession, evaluation: CompetitiveEvaluation):
        self.session = session
        self.evaluation = evaluation
        self.timestamp = datetime.now()
    
    def get_final_python_code(self) -> Optional[str]:
        """Get the final Python implementation."""
        if self.session.python_implementations:
            return self.session.python_implementations[-1].code
        return None
    
    def get_final_typescript_code(self) -> Optional[str]:
        """Get the final TypeScript implementation."""
        if self.session.typescript_implementations:
            return self.session.typescript_implementations[-1].code
        return None
    
    def get_winner(self) -> str:
        """Get the winning language."""
        return self.evaluation.winner
    
    def get_score_summary(self) -> str:
        """Get a summary of the scores."""
        return f"Python: {self.evaluation.python_total_score:.1f}/10, TypeScript: {self.evaluation.typescript_total_score:.1f}/10"


class GACCIAComplete:
    """Complete GACCIA system combining competitive coding and evaluation."""
    
    def __init__(self, use_koyeb: bool = False):
        """
        Initialize GACCIA with optional Koyeb model support.
        
        Args:
            use_koyeb: If True, use Koyeb-hosted models for one of the agent types
        """
        self.use_koyeb = use_koyeb
        self.orchestrator = GACCIAOrchestrator(use_koyeb=use_koyeb)
        self.evaluator = EvaluationOrchestrator(use_koyeb=use_koyeb)
    
    def run_complete_competition(
        self,
        code: str,
        language: str,
        rounds: int = 2,
        logger: Optional[ResultsLogger] = None,
    ) -> CompletedGACCIASession:
        """Run a complete competitive session with evaluation."""
        
        print("🚀 GACCIA: Generative Adversarial Competitive Code Improvement")
        print("=" * 80)
        print(f"Starting with {language} code, running {rounds} competitive rounds...")
        
        # Show model configuration
        if self.use_koyeb:
            print("🌐 Using Koyeb-hosted models for evaluation agents")
        else:
            print("🤖 Using OpenAI models for all agents")
        print()
        
        # Phase 1: Competitive Development
        print("🥊 PHASE 1: COMPETITIVE DEVELOPMENT")
        print("-" * 50)
        if logger is None:
            logger = ResultsLogger("gaccia_run")

        session = self.orchestrator.run_competitive_session(
            code, language, rounds, logger=logger
        )
        
        # Phase 2: Evaluation
        print("\n🏆 PHASE 2: COMPETITIVE EVALUATION")
        print("-" * 50)
        
        # Get final implementations for evaluation
        final_python = session.python_implementations[-1].code if session.python_implementations else code if language.lower() == "python" else ""
        final_typescript = session.typescript_implementations[-1].code if session.typescript_implementations else code if language.lower() == "typescript" else ""
        
        if not final_python or not final_typescript:
            print("❌ Error: Missing implementations for evaluation")
            return None
        
        # Run evaluation
        evaluation = self.evaluator.evaluate_implementations(final_python, final_typescript)

        logger.log_evaluation(evaluation)

        # Create completed session
        completed_session = CompletedGACCIASession(session, evaluation)

        logger.save_summary(session, evaluation)
        
        # Print results
        self._print_final_results(completed_session)
        
        return completed_session
    
    def _print_final_results(self, completed_session: CompletedGACCIASession):
        """Print the final results summary."""
        print("\n" + "🎉" * 20 + " FINAL RESULTS " + "🎉" * 20)
        print()
        
        print(f"📊 Score Summary: {completed_session.get_score_summary()}")
        print(f"🏆 Winner: {completed_session.get_winner()}")
        print()
        
        print("💬 Competitive Snark:")
        print(f"🐍 Python says: {completed_session.evaluation.python_snark}")
        print(f"📘 TypeScript says: {completed_session.evaluation.typescript_snark}")
        print()
        
        print("📈 Round Summary:")
        print(f"   • Python implementations: {len(completed_session.session.python_implementations)}")
        print(f"   • TypeScript implementations: {len(completed_session.session.typescript_implementations)}")
        print()
        
        # Show code evolution
        if completed_session.session.original_language == "python":
            print("🔄 Code Evolution: Python → TypeScript → Python")
        else:
            print("🔄 Code Evolution: TypeScript → Python → TypeScript")
        
        print("\n" + "=" * 80)
    
    def save_complete_results(self, completed_session: CompletedGACCIASession, custom_name: Optional[str] = None) -> Path:
        """Save all results from the completed session."""
        
        # Create results directory
        session_name = custom_name or f"gaccia_session_{completed_session.session.session_id[:8]}"
        results_dir = Path("results") / session_name
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Save original code
        original_ext = "py" if completed_session.session.original_language == "python" else "ts"
        with open(results_dir / f"01_original.{original_ext}", "w") as f:
            f.write(completed_session.session.original_code)
        
        # Save all implementations
        for i, impl in enumerate(completed_session.session.python_implementations, 1):
            with open(results_dir / f"0{i+1}_python_v{impl.version}.py", "w") as f:
                f.write(impl.code)
        
        for i, impl in enumerate(completed_session.session.typescript_implementations, 1):
            with open(results_dir / f"0{i+1}_typescript_v{impl.version}.ts", "w") as f:
                f.write(impl.code)
        
        # Save evaluation results
        self.evaluator.save_evaluation_report(completed_session.evaluation, results_dir)
        
        # Save session metadata
        session_data = {
            "session_id": completed_session.session.session_id,
            "original_language": completed_session.session.original_language,
            "created_at": completed_session.session.created_at.isoformat(),
            "completed_at": completed_session.timestamp.isoformat(),
            "rounds_completed": max(len(completed_session.session.python_implementations), 
                                  len(completed_session.session.typescript_implementations)),
            "winner": completed_session.evaluation.winner,
            "final_scores": {
                "python": completed_session.evaluation.python_total_score,
                "typescript": completed_session.evaluation.typescript_total_score
            },
            "competitive_snark": {
                "python": completed_session.evaluation.python_snark,
                "typescript": completed_session.evaluation.typescript_snark
            }
        }
        
        with open(results_dir / "session_metadata.json", "w") as f:
            json.dump(session_data, f, indent=2)
        
        # Create a summary report
        with open(results_dir / "README.md", "w") as f:
            f.write(self._generate_markdown_report(completed_session))
        
        print(f"📁 Complete results saved to: {results_dir}")
        return results_dir
    
    def _generate_markdown_report(self, completed_session: CompletedGACCIASession) -> str:
        """Generate a markdown report of the session."""
        return f"""# GACCIA Session Report

**Session ID:** `{completed_session.session.session_id}`  
**Date:** {completed_session.timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Original Language:** {completed_session.session.original_language.title()}  

## 🏆 Final Results

**Winner:** {completed_session.evaluation.winner}  
**Final Scores:**
- 🐍 Python: {completed_session.evaluation.python_total_score:.1f}/10
- 📘 TypeScript: {completed_session.evaluation.typescript_total_score:.1f}/10

## 💬 Competitive Snark

**🐍 Python's take:** {completed_session.evaluation.python_snark}  
**📘 TypeScript's take:** {completed_session.evaluation.typescript_snark}

## 📊 Detailed Scores

### Python Evaluation
{self._format_evaluations_for_markdown(completed_session.evaluation.python_evaluations)}

### TypeScript Evaluation  
{self._format_evaluations_for_markdown(completed_session.evaluation.typescript_evaluations)}

## 🔄 Code Evolution

Original language: {completed_session.session.original_language.title()}  
Rounds completed: {max(len(completed_session.session.python_implementations), len(completed_session.session.typescript_implementations))}  

This session demonstrates the competitive improvement process where code is iteratively 
converted between Python and TypeScript, with each language's advocates trying to 
create the best possible implementation in their preferred language.

---
*Generated by GACCIA - Generative Adversarial Competitive Code Improvement Agent*
"""
    
    def _format_evaluations_for_markdown(self, evaluations) -> str:
        """Format evaluations for markdown display."""
        lines = []
        for eval in evaluations:
            lines.append(f"- **{eval.dimension}:** {eval.score:.1f}/10")
        return "\n".join(lines)


# Pre-defined example codes for testing
EXAMPLE_CODES = {
    "fibonacci": {
        "python": '''
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
''',
        "typescript": '''
function fibonacci(n: number): number {
    // Calculate the nth Fibonacci number
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

function main(): void {
    for (let i = 0; i < 10; i++) {
        console.log(`fib(${i}) = ${fibonacci(i)}`);
    }
}

main();
'''
    },
    "weather_api": {
        "python": '''
import requests
from typing import Dict, Any

def get_weather(city: str, api_key: str) -> Dict[str, Any]:
    """Fetch weather data for a city."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()

def format_weather(weather_data: Dict[str, Any]) -> str:
    """Format weather data for display."""
    city = weather_data["name"]
    temp = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    
    return f"Weather in {city}: {temp}°C, {description}"
''',
        "typescript": '''
interface WeatherData {
    name: string;
    main: {
        temp: number;
    };
    weather: Array<{
        description: string;
    }>;
}

async function getWeather(city: string, apiKey: string): Promise<WeatherData> {
    const baseUrl = "http://api.openweathermap.org/data/2.5/weather";
    const params = new URLSearchParams({
        q: city,
        appid: apiKey,
        units: "metric"
    });
    
    const response = await fetch(`${baseUrl}?${params}`);
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
}

function formatWeather(weatherData: WeatherData): string {
    const { name, main: { temp }, weather } = weatherData;
    const description = weather[0].description;
    
    return `Weather in ${name}: ${temp}°C, ${description}`;
}
'''
    }
}


def main():
    """Main CLI interface for GACCIA."""
    
    if len(sys.argv) < 2:
        print("🚀 GACCIA - Generative Adversarial Competitive Code Improvement")
        print()
        print("Usage:")
        print("  python gaccia_main.py <example_name> [language] [rounds] [--use-koyeb]")
        print()
        print("Available examples:")
        for name in EXAMPLE_CODES.keys():
            print(f"  - {name}")
        print()
        print("Languages: python, typescript")
        print("Rounds: number of competitive rounds (default: 2)")
        print("--use-koyeb: Use Koyeb-hosted models for evaluation agents")
        print()
        print("Example: python gaccia_main.py fibonacci python 3")
        print("Example: python gaccia_main.py fibonacci python 3 --use-koyeb")
        return
    
    # Parse arguments
    example_name = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "python"
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    use_koyeb = "--use-koyeb" in sys.argv
    
    if example_name not in EXAMPLE_CODES:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(EXAMPLE_CODES.keys())}")
        return
    
    if language not in ["python", "typescript"]:
        print(f"❌ Unknown language: {language}")
        print("Available languages: python, typescript")
        return
    
    # Get the example code
    code = EXAMPLE_CODES[example_name][language]
    
    # Initialize and run GACCIA
    gaccia = GACCIAComplete(use_koyeb=use_koyeb)
    
    try:
        # Run the complete competition
        logger = ResultsLogger(f"{example_name}_{language}")
        completed_session = gaccia.run_complete_competition(
            code, language, rounds, logger=logger
        )

        if completed_session:
            print(f"\n✅ Competition completed successfully!")
            print(f"📁 View detailed results in: {logger.base_dir}")
            print(f"📖 Open {logger.base_dir}/SUMMARY.md for a summary report")
        
    except KeyboardInterrupt:
        print("\n⏹️  Competition stopped by user.")
    except Exception as e:
        print(f"\n❌ Error during competition: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()