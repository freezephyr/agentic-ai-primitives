import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src/agentic_learning/agentic_loop_with_RAG/RAG_earning_rpt_QnA_Eval.py"
)


def load_eval_module():
    spec = importlib.util.spec_from_file_location("rag_eval_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_run_rag_query_tests_uses_question_field(monkeypatch):
    module = load_eval_module()
    calls = []

    def fake_answer_question(collection, question, n_results):
        calls.append((collection, question, n_results))
        return f"answer:{question}"

    monkeypatch.setattr(module, "answer_question", fake_answer_question)

    tests = [{"Test_id": 1, "Question": "who owns Wonderkid wonderland", "Expected": "n/a"}]
    result = module.run_rag_query_tests("collection", tests, 3)

    assert result == ["answer:who owns Wonderkid wonderland"]
    assert calls == [("collection", "who owns Wonderkid wonderland", 3)]
