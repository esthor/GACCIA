# uv run gaccia_agents_with_images.py demo

"""
GACCIA with Live Image Generation

Integrates image generation throughout the competitive coding battle
to create an engaging, entertaining user experience.
"""

import asyncio
import base64
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from openai import OpenAI

from gaccia_agents import (
    GACCIAOrchestrator,
    GACCIASession,
    CodeImplementation,
    ImageGenerationAgent,
)
from gaccia_evaluators import EvaluationOrchestrator, CompetitiveEvaluation
from gaccia_main import CompletedGACCIASession


class EnhancedGACCIAOrchestrator(GACCIAOrchestrator):
    """Enhanced orchestrator with live image generation during battles."""

    def __init__(self):
        super().__init__()
        self.image_agent = ImageGenerationAgent()
        self.openai_client = OpenAI()  # Will use OPENAI_API_KEY from env
        self.generated_images = {}  # Store image URLs/paths
        self.evaluator = EvaluationOrchestrator()  # Add evaluator
        self.results_dir: Optional[Path] = None

    def run_competitive_session_with_images(
        self, code: str, language: str, rounds: int = 2
    ) -> tuple[GACCIASession, Dict[str, str]]:
        """Run competitive session with live image generation."""

        print("🎬 Starting GACCIA Battle with Live Image Generation!")
        print("=" * 70)

        # Generate battle announcement image
        self._generate_battle_start_image(language, rounds)

        # Run the main competitive session
        session = GACCIASession(original_code=code, original_language=language.lower())

        # Prepare results directory for this session
        self.results_dir = Path("results") / f"gaccia_with_images_{session.session_id[:8]}"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        (self.results_dir / "rounds").mkdir(parents=True, exist_ok=True)
        (self.results_dir / "evaluations").mkdir(parents=True, exist_ok=True)

        current_code = code
        current_language = language.lower()

        for round_num in range(rounds):
            print(f"\n🥊 ROUND {round_num + 1}/{rounds} - THE BATTLE INTENSIFIES!")
            print("-" * 50)

            # Generate round start image
            self._generate_round_start_image(round_num + 1, current_language)

            # Determine target language
            target_language = "typescript" if current_language == "python" else "python"

            # Run the conversion flow with live updates
            implementation = self._run_language_conversion_flow_with_images(
                current_code, current_language, target_language, round_num + 1
            )

            # Store implementation
            if target_language == "python":
                session.python_implementations.append(implementation)
            else:
                session.typescript_implementations.append(implementation)

            # Persist implementation for this round
            if self.results_dir is not None:
                ext = "py" if target_language == "python" else "ts"
                round_path = self.results_dir / "rounds" / f"round_{round_num + 1}_{target_language}.{ext}"
                with open(round_path, "w") as f:
                    f.write(implementation.code)

            # Generate round completion image
            self._generate_round_completion_image(
                round_num + 1, target_language, implementation
            )

            # Update for next round
            current_code = implementation.code
            current_language = target_language

            print(
                f"✅ Round {round_num + 1} complete: {current_language} wins this round!"
            )

        # Generate final battle completion image
        self._generate_battle_completion_image(session)

        return session, self.generated_images

    def _generate_battle_start_image(self, starting_language: str, rounds: int):
        """Generate an epic battle start image."""
        print("🎨 Generating epic battle announcement...")

        prompt = self.image_agent.generate_battle_prompt(
            f"Epic coding battle starting! {starting_language.title()} vs the world, {rounds} rounds of competitive programming"
        )

        image_url = self._create_image(prompt, "battle_start")
        print(f"🖼️  Battle announcement ready! {image_url}")

    def _generate_round_start_image(self, round_num: int, current_language: str):
        """Generate round start hype image."""
        print(f"🎨 Generating Round {round_num} hype image...")

        other_lang = "TypeScript" if current_language == "python" else "Python"
        prompt = f"""
        Create an epic sports-style image for Round {round_num} of a coding battle.
        Show {current_language.title()} preparing to face {other_lang} in combat.
        Style: dramatic, competitive, like a boxing match or video game battle screen.
        Include: round number, languages as fighters, intense atmosphere.
        Colors: vibrant, high energy. Make it look like a championship fight.
        """

        image_url = self._create_image(prompt, f"round_{round_num}_start")
        print(f"🥊 Round {round_num} hype image ready!")

    def _generate_round_completion_image(
        self, round_num: int, winning_language: str, implementation: CodeImplementation
    ):
        """Generate round completion victory image."""
        print(f"🎨 Generating Round {round_num} victory image...")

        prompt = f"""
        Create a victory celebration image for {winning_language.title()} winning Round {round_num}.
        Style: triumphant, celebratory, like a sports victory moment.
        Show {winning_language.title()} as the champion with trophy or victory pose.
        Include: confetti, victory elements, "ROUND {round_num} WINNER" text.
        Colors: gold, bright, celebratory. Make it feel like a championship win.
        """

        image_url = self._create_image(prompt, f"round_{round_num}_victory")
        print(f"🏆 {winning_language.title()} victory image ready!")

    def _generate_battle_completion_image(self, session: GACCIASession):
        """Generate final battle results image."""
        print("🎨 Generating final battle results image...")

        python_count = len(session.python_implementations)
        typescript_count = len(session.typescript_implementations)

        prompt = f"""
        Create an epic final results image for a coding battle.
        Python appeared in {python_count} implementations.
        TypeScript appeared in {typescript_count} implementations.
        Style: grand finale, championship results, dramatic and exciting.
        Include: both language logos, final scores, epic background.
        Make it feel like the end of an amazing competition.
        """

        image_url = self._create_image(prompt, "battle_finale")
        print("🎊 Final battle results image ready!")

    def _run_language_conversion_flow_with_images(
        self, code: str, source_lang: str, target_lang: str, version: int
    ) -> CodeImplementation:
        """Enhanced conversion flow with live image generation."""

        print(f"⚔️  {source_lang.title()} challenges {target_lang.title()}!")

        # Generate "thinking" image while agents work
        self._generate_thinking_image(source_lang, target_lang)

        # Step 1: Source language architect analyzes the code
        print("🧠 Analyzing the challenger's code...")
        if source_lang == "python":
            analysis = self.python_architect.analyze_code(code, source_lang)
        else:
            analysis = self.typescript_architect.analyze_code(code, source_lang)

        # Step 2: Polyglot architect creates conversion plan
        print("📋 The judges are planning the counter-attack...")
        conversion_plan = self.polyglot_architect.create_conversion_plan(
            analysis, target_lang
        )

        # Generate strategy image
        self._generate_strategy_image(source_lang, target_lang)

        # Step 3: Target language architect plans implementation
        print(f"🏗️  {target_lang.title()} architect is crafting the perfect response...")
        if target_lang == "python":
            implementation_plan = self.python_architect.plan_implementation(
                analysis, conversion_plan
            )
        else:
            implementation_plan = self.typescript_architect.plan_implementation(
                analysis, conversion_plan
            )

        # Step 4: Target language coder implements
        print(f"⚡ {target_lang.title()} coder is writing the ultimate solution...")
        if target_lang == "python":
            implemented_code = self.python_coder.implement_code(
                implementation_plan, code
            )
        else:
            implemented_code = self.typescript_coder.implement_code(
                implementation_plan, code
            )

        # Generate coding action image
        self._generate_coding_action_image(target_lang)

        # Step 5: Target language architect reviews
        print("🔍 Quality control in progress...")
        if target_lang == "python":
            review = self.python_architect.review_implementation(implemented_code)
        else:
            review = self.typescript_architect.review_implementation(implemented_code)

        # Step 6: Polyglot architect validates conversion
        print("⚖️  The judges are making their final verdict...")
        conversion_review = self.polyglot_architect.review_conversion(
            code, implemented_code, source_lang, target_lang
        )

        return CodeImplementation(
            code=implemented_code,
            language=target_lang,
            version=version,
            improvements=[],
            architect_notes=f"Review: {review}\n\nConversion Review: {conversion_review}",
        )

    def _generate_thinking_image(self, source_lang: str, target_lang: str):
        """Generate image of agents 'thinking' and strategizing."""
        print("🤔 Agents are strategizing...")

        prompt = f"""
        Create an image showing AI agents deep in thought, planning how to convert 
        {source_lang.title()} code to {target_lang.title()}.
        Style: thoughtful, strategic, like chess masters planning moves.
        Include: gears turning, lightbulbs, strategy boards, focused concentration.
        Colors: cool blues and whites for thinking, technical aesthetic.
        """

        self._create_image(prompt, f"thinking_{source_lang}_to_{target_lang}")

    def _generate_strategy_image(self, source_lang: str, target_lang: str):
        """Generate strategic planning image."""
        print("📊 Strategy session in progress...")

        prompt = f"""
        Create an image of a strategic war room where experts are planning how to 
        defeat {source_lang.title()} using {target_lang.title()}.
        Style: high-tech command center, strategic planning, battle tactics.
        Include: monitors, code snippets, battle plans, focused team.
        Colors: green matrix-style for tech, dramatic lighting.
        """

        self._create_image(prompt, f"strategy_{source_lang}_vs_{target_lang}")

    def _generate_coding_action_image(self, language: str):
        """Generate action-packed coding image."""
        print("💻 Code is being written at lightning speed...")

        prompt = f"""
        Create a dynamic action image of intense {language.title()} coding in progress.
        Style: fast-paced, energetic, like an action movie scene.
        Include: flying code, fast typing, sparks, energy, determination.
        Colors: bright, electric, high energy. Make coding look epic and exciting.
        """

        self._create_image(prompt, f"coding_action_{language}")

    def _create_image(self, prompt: str, filename: str) -> Optional[str]:
        """Create image using OpenAI's image generation."""
        try:
            response = self.openai_client.responses.create(
                model="gpt-4.1",
                input=prompt,
                tools=[{"type": "image_generation", "quality": "low", "size": "1024x1024"}],
                # stream=True,
                # tools=[{"type": "image_generation", "partial_images": 2}],
            )
            image_data = [
                output.result
                for output in response.output
                if output.type == "image_generation_call"
            ]

            # Download and save the image
            saved_path = self._download_and_save_image(image_data, filename)

            # Store in our tracking dict
            self.generated_images[filename] = saved_path

            return saved_path

        except Exception as e:
            print(f"⚠️  Image generation failed: {e}")
            return None

    def _download_and_save_image(self, image_data: list, filename: str) -> str:
        """Download image and save to results directory."""
        try:
            # Create images directory
            images_dir = Path("results") / "battle_images"
            images_dir.mkdir(parents=True, exist_ok=True)

            for idx, image_base64 in enumerate(image_data):
                # Decode and save each image
                image_bytes = base64.b64decode(image_base64)
                with open(images_dir / f"{filename}_{idx}.png", "wb") as f:
                    f.write(image_bytes)

            print(f"💾 Images saved to: {images_dir}")

            return str(images_dir)

        except Exception as e:
            print(f"⚠️  Failed to save image: {e}")
            return image_data  # Return original URL as fallback

    def run_complete_competition_with_images(
        self, code: str, language: str, rounds: int = 2
    ) -> tuple[CompletedGACCIASession, Dict[str, str]]:
        """Run a complete competitive session with evaluation and live image generation."""

        print("🚀 GACCIA: Generative Adversarial Competitive Code Improvement")
        print("🎨 WITH LIVE IMAGE GENERATION!")
        print("=" * 80)
        print(f"Starting with {language} code, running {rounds} competitive rounds...")
        print()

        # Phase 1: Competitive Development with Images
        print("🥊 PHASE 1: COMPETITIVE DEVELOPMENT WITH LIVE IMAGES")
        print("-" * 60)
        session, images = self.run_competitive_session_with_images(code, language, rounds)

        # Phase 2: Evaluation
        print("\n🏆 PHASE 2: COMPETITIVE EVALUATION")
        print("-" * 50)

        # Get final implementations for evaluation
        final_python = session.python_implementations[-1].code if session.python_implementations else code if language.lower() == "python" else ""
        final_typescript = session.typescript_implementations[-1].code if session.typescript_implementations else code if language.lower() == "typescript" else ""

        if not final_python or not final_typescript:
            raise ValueError("Need both Python and TypeScript implementations for evaluation!")

        # Run evaluation
        evaluation = self.evaluator.evaluate_implementations(
            final_python,
            final_typescript,
            results_dir=self.results_dir,
        )

        # Create completed session
        completed_session = CompletedGACCIASession(session, evaluation)

        # Print results
        self._print_final_results(completed_session)

        # Save complete results
        self._save_complete_results_with_images(completed_session, images)

        return completed_session, images

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

    def _save_complete_results_with_images(self, completed_session: CompletedGACCIASession, images: Dict[str, str]):
        """Save all results including code files, evaluations, and images."""

        # Create results directory if not already set
        session_name = f"gaccia_with_images_{completed_session.session.session_id[:8]}"
        results_dir = self.results_dir or Path("results") / session_name
        results_dir.mkdir(parents=True, exist_ok=True)
        (results_dir / "rounds").mkdir(parents=True, exist_ok=True)
        (results_dir / "evaluations").mkdir(parents=True, exist_ok=True)

        print(f"\n💾 Saving complete results to: {results_dir}")

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

        # Save session metadata (including image info)
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
            },
            "generated_images": images
        }

        with open(results_dir / "session_metadata.json", "w") as f:
            json.dump(session_data, f, indent=2)

        # Create a summary report
        with open(results_dir / "README.md", "w") as f:
            f.write(self._generate_markdown_report_with_images(completed_session, images))

        print(f"📁 Complete results saved to: {results_dir}")
        print(f"🖼️  Battle images saved to: {results_dir}/battle_images/")
        return results_dir

    def _generate_markdown_report_with_images(self, completed_session: CompletedGACCIASession, images: Dict[str, str]) -> str:
        """Generate a markdown report of the session including images."""
        
        original_ext = "py" if completed_session.session.original_language == "python" else "ts"
        
        images_section = "\n## 🎨 Battle Images\n\n"
        for name, path in images.items():
            # Make path relative to the README location
            relative_path = Path(path).name if "/" in path else path
            images_section += f"### {name.replace('_', ' ').title()}\n"
            images_section += f"![{name}](battle_images/{relative_path})\n\n"

        return f"""# GACCIA Session Report WITH IMAGES 🎨

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

{images_section}

## 📊 Implementation Details

### Original Code ({completed_session.session.original_language.title()})
```{original_ext}
{completed_session.session.original_code}
```

### Final Python Implementation
```python
{completed_session.get_final_python_code() or "No Python implementation"}
```

### Final TypeScript Implementation
```typescript
{completed_session.get_final_typescript_code() or "No TypeScript implementation"}
```

---
*Generated by GACCIA with Live Image Generation*
"""

def run_enhanced_battle_demo():
    """Run an enhanced battle demo with live image generation."""

    # Enhanced orchestrator with images
    orchestrator = EnhancedGACCIAOrchestrator()

    # Example code for battle
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

    print("🎪 WELCOME TO THE ULTIMATE CODING BATTLE!")
    print("🎯 Python vs TypeScript - Who will reign supreme?")
    print("🎨 With live image generation for maximum entertainment!")
    print()

    try:
        # Run the enhanced battle with complete evaluation
        completed_session, images = orchestrator.run_complete_competition_with_images(
            demo_code, "python", rounds=1
        )

        print("\n" + "🎉" * 25)
        print("🏆 BATTLE COMPLETE! 🏆")
        print("🎉" * 25)
        print()

        print("📊 Battle Statistics:")
        print(f"   • Session ID: {completed_session.session.session_id}")
        print(f"   • Python implementations: {len(completed_session.session.python_implementations)}")
        print(
            f"   • TypeScript implementations: {len(completed_session.session.typescript_implementations)}"
        )
        print(f"   • Images generated: {len(images)}")
        print(f"   • Final winner: {completed_session.get_winner()}")
        print(f"   • Final scores: {completed_session.get_score_summary()}")
        print()

        print("🖼️  Generated Images:")
        for name, path in images.items():
            print(f"   • {name}: {path}")

        print("\n📁 All results saved with complete evaluation!")
        print("🎬 Check out the epic battle images and detailed reports!")

    except KeyboardInterrupt:
        print("\n⏹️  Battle interrupted by user!")
    except Exception as e:
        print(f"\n❌ Battle error: {e}")
        import traceback

        traceback.print_exc()


# Command line interface for uv run
def main():
    """Main entry point for uv run."""

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_enhanced_battle_demo()
    else:
        print("Usage: uv run gaccia_with_images.py demo")
        print("This will run the enhanced battle with live image generation!")


if __name__ == "__main__":
    main()
