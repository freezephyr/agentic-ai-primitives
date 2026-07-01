# The Tool-vs-Answer Decision Seam

An LLM with tools faces a fundamental choice on every user request: answer from
its own knowledge, or call a function. This seam — the decision boundary between
knowing and fetching — is where agentic behavior begins.

## What this teaches

- **Tool descriptions shape model behavior.** The `check_weather` description
  says "dont use this function at all costs. use forecast function." Watch how
  the model weighs this guidance alongside the actual tool choice.
- **Multi-turn tool resolution.** When asked about two cities, the model may
  call a tool once per city. Each call feeds back into the conversation before
  the final answer.
- **The boundaries of tool awareness.** When an unrelated question ("whats
  2+2?") follows a tool-grounded conversation, does the model still reach for
  tools, or does it answer directly?

## How to run

```powershell
python example.py
```

Requires `litellm` and a configured Bedrock provider (see project root `.env`).
