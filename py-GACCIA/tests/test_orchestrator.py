import sys
import types
from pathlib import Path

# create minimal stubs for missing external dependencies
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

from gaccia_agents import GACCIAOrchestrator, CodeImplementation

class DummyOrchestrator(GACCIAOrchestrator):
    def __init__(self):
        pass  # skip parent init to avoid heavy dependencies
    def _run_language_conversion_flow(self, code, source_lang, target_lang, version):
        return CodeImplementation(code=f"{target_lang}_v{version}", language=target_lang, version=version, improvements=[], architect_notes="")

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def test_conversion_loop_alternates_languages():
    code = (DATA_DIR / "python_example.py").read_text()
    orchestrator = DummyOrchestrator()
    session = orchestrator.run_competitive_session(code, "python", rounds=2)

    assert len(session.python_implementations) == 1
    assert len(session.typescript_implementations) == 1
    assert session.python_implementations[0].language == "python"
    assert session.typescript_implementations[0].language == "typescript"
