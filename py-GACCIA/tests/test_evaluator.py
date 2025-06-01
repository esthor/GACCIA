import sys
import types
from pathlib import Path

# stub external packages as in orchestrator test
agno = types.ModuleType('agno')
agent_mod = types.ModuleType('agno.agent')
models_mod = types.ModuleType('agno.models')
openai_mod = types.ModuleType('agno.models.openai')
openai_like_mod = types.ModuleType('agno.models.openai.like')
dotenv_mod = types.ModuleType('dotenv')
def load_dotenv(*args, **kwargs):
    pass
dotenv_mod.load_dotenv = load_dotenv

class DummyAgent:
    def __init__(self, *args, **kwargs):
        pass
    def run(self, prompt):
        class R:
            content = "dummy"
        return R()

class DummyModel:
    def __init__(self, *args, **kwargs):
        pass

agent_mod.Agent = DummyAgent
openai_mod.OpenAIChat = DummyModel
openai_like_mod.OpenAILike = DummyModel
models_mod.openai = openai_mod
sys.modules['agno'] = agno
sys.modules['agno.agent'] = agent_mod
sys.modules['agno.models'] = models_mod
sys.modules['agno.models.openai'] = openai_mod
sys.modules['agno.models.openai.like'] = openai_like_mod
sys.modules['dotenv'] = dotenv_mod

from gaccia_evaluators import EvaluationOrchestrator, DetailedEvaluation, CompetitiveEvaluation

class SimpleJudge:
    def __init__(self, dimension):
        self.dimension = dimension
    def evaluate(self, code, language):
        return DetailedEvaluation(
            dimension=self.dimension,
            score=5.0,
            reasoning="ok",
            strengths=[],
            weaknesses=[],
            suggestions=[],
        )

class DummySnark:
    def __init__(self, language):
        self.language = language
    def generate_snark(self, code, summary):
        return f"snark {self.language}"

class DummyEvaluator(EvaluationOrchestrator):
    def __init__(self):
        self.python_judges = {"readability": SimpleJudge("Readability")}
        self.typescript_judges = {"readability": SimpleJudge("Readability")}
        self.python_snark = DummySnark("python")
        self.typescript_snark = DummySnark("typescript")

def test_evaluator_schema():
    evaluator = DummyEvaluator()
    result = evaluator.evaluate_implementations("print('hi')", "console.log('hi')")

    assert isinstance(result, CompetitiveEvaluation)
    assert isinstance(result.python_evaluations, list)
    assert isinstance(result.typescript_evaluations, list)
    assert isinstance(result.python_total_score, float)
    assert isinstance(result.typescript_total_score, float)
    assert isinstance(result.winner, str)
    assert isinstance(result.python_snark, str)
    assert isinstance(result.typescript_snark, str)
