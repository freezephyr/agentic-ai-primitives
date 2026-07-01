# Intent Routing for Tiered Model Selection

Not every question needs a 100B-parameter model. Routing is the pattern of
using a cheap classifier to decide how much compute a request deserves.

## What this teaches

- **Classification before execution.** A lightweight model (Nova Micro)
  determines whether a request is "simple" or "complex" based on whether the
  available tools can handle it.
- **Cost-aware dispatching.** Simple intents stay on the cheap model; complex
  ones get escalated to a larger model (Qwen3 Coder). This is the core
  economics of production agents.
- **Routing prompt design.** The router's prompt must define "simple" and
  "complex" strictly in terms of tool coverage, not model knowledge. If the
  router uses its own implicit knowledge, the tiering breaks.

## How to run

```powershell
python example.py
```

Observe the routing response: it outputs a classification and confidence
probability before any task-specific inference runs.
