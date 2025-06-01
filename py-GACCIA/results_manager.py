from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from gaccia_agents import CodeImplementation, GACCIASession
from gaccia_evaluators import CompetitiveEvaluation, EvaluationOrchestrator


class ResultsLogger:
    """Utility to log intermediate and final GACCIA results."""

    def __init__(self, session_name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_dir = Path(__file__).parent / "results" / f"{timestamp}_{session_name}"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def log_round(self, round_num: int, impl: CodeImplementation) -> None:
        """Save implementation details for a round."""
        round_dir = self.base_dir / f"round_{round_num}"
        round_dir.mkdir(parents=True, exist_ok=True)
        ext = "py" if impl.language == "python" else "ts"
        with open(round_dir / f"implementation_v{impl.version}.{ext}", "w") as f:
            f.write(impl.code)
        with open(round_dir / "notes.md", "w") as f:
            f.write(impl.architect_notes or "")

    def log_image_prompts(self, prompts: Dict[str, str]) -> None:
        """Save any generated image prompts."""
        if prompts:
            with open(self.base_dir / "image_prompts.json", "w") as f:
                json.dump(prompts, f, indent=2)

    def log_evaluation(self, evaluation: CompetitiveEvaluation) -> None:
        """Save evaluation report and snark."""
        EvaluationOrchestrator().save_evaluation_report(evaluation, self.base_dir)
        with open(self.base_dir / "snark.md", "w") as f:
            f.write(f"**🐍 Python's take:** {evaluation.python_snark}\n\n")
            f.write(f"**📘 TypeScript's take:** {evaluation.typescript_snark}\n")

    def save_summary(self, session: GACCIASession, evaluation: CompetitiveEvaluation) -> None:
        """Write a summary markdown combining all results."""
        summary = self._generate_summary(session, evaluation)
        with open(self.base_dir / "SUMMARY.md", "w") as f:
            f.write(summary)

    def _generate_summary(self, session: GACCIASession, evaluation: CompetitiveEvaluation) -> str:
        rounds = max(len(session.python_implementations), len(session.typescript_implementations))
        return f"""# GACCIA Session Summary

**Session ID:** `{session.session_id}`
**Started:** {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}
**Rounds:** {rounds}

## 🏆 Final Results

**Winner:** {evaluation.winner}
**Scores:** Python {evaluation.python_total_score:.1f}/10 vs TypeScript {evaluation.typescript_total_score:.1f}/10

## 💬 Competitive Snark

- Python: {evaluation.python_snark}
- TypeScript: {evaluation.typescript_snark}

Detailed evaluation scores and code for each round can be found in the subfolders of this run.
"""

