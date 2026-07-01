# Agent Loop Primitives

Before adding tools, routers, or RAG, an agent needs three things: a loop, a
guard, and a score. This lesson extracts the minimal reusable building blocks.

## What this teaches

- **The plan-act-reflect loop (`AgentLoop`).** A generic runner that accepts a
  planner and a responder as callables. The loop itself owns no logic — it's a
  protocol that any agent shape can implement.
- **Policy-as-code (`GovernancePolicy`).** Prefix-based action blocking that
  runs *before* execution. Shows how to model guardrails as simple string
  matchers (extensible to regex, embedding similarity, etc.).
- **Evaluation harness (`EvaluationCase`, `EvaluationReport`).** A pure-data
  approach to testing: given input → expected output, run a function and report
  pass/fail with a score.

## How to use

This lesson is a Python package. Install it (from project root):

```powershell
pip install -e .
```

Then import in your own experiments:

```python
from agentic_learning.agent_loop import AgentLoop
from agentic_learning.governance import GovernancePolicy
from agentic_learning.evals import run_evaluation_suite
```

## Package structure

```
agentic_learning/
  __init__.py       — re-exports the three primitives
  agent_loop.py     — AgentContext, AgentAction, AgentOutput, AgentLoop
  evals.py          — EvaluationCase, EvaluationReport, run_evaluation_suite
  governance.py     — GovernanceDecision, GovernanceResult, GovernancePolicy
```
