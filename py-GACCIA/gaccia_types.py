"""
Shared types and dataclasses for the GACCIA project.

This module contains the core data structures used across the GACCIA
agent system to avoid circular imports.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class CodeImplementation:
    """Represents a code implementation with metadata."""

    code: str
    language: str
    version: int
    improvements: List[str]
    architect_notes: str


@dataclass
class EvaluationResult:
    """Represents evaluation results from judges."""

    readability_score: float
    maintainability_score: float
    latest_tools_score: float
    docs_enjoyability_score: float
    security_performance_score: float
    overall_score: float
    comments: str
    snark: str  # For the snarky comments about the other language


@dataclass
class GACCIASession:
    """Represents a complete GACCIA session."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    original_code: str = ""
    original_language: str = ""
    python_implementations: List[CodeImplementation] = field(default_factory=list)
    typescript_implementations: List[CodeImplementation] = field(default_factory=list)
    evaluations: List[EvaluationResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class LanguageConversionMap:
    """Maps between programming language features and libraries."""

    syntax_mappings: Dict[str, str]
    library_mappings: Dict[str, str]
