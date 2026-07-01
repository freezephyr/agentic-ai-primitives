# Agentic Learning Workspace

A collection of hands-on lessons exploring AI agentic primitives — from
tool-calling seams to RAG evaluation. Each lesson is a self-contained folder
with its own README explaining the concept it teaches.

## Lessons

| # | Folder | The Lesson |
|---|--------|------------|
| 01 | [tool-calling-seam](lessons/01-tool-calling-seam/) | When an LLM decides to answer vs call a tool |
| 02 | [intent-routing](lessons/02-intent-routing/) | Routing requests to the right model by complexity |
| 03 | [rag-pipeline](lessons/03-rag-pipeline/) | Full RAG flow: PDF → chunks → retrieve → answer |
| 04 | [rag-evaluation](lessons/04-rag-evaluation/) | LLM-as-judge scoring for RAG quality |
| 05 | [agent-loop-primitives](lessons/05-agent-loop-primitives/) | Minimal reusable loop, governance, and eval building blocks |

## Getting started

```powershell
pip install -e .
pytest
```

Each lesson's folder contains its own run instructions.
