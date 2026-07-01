# Retrieval-Augmented Generation from Scratch

RAG is the simplest pattern that makes an LLM ground its answers in external
data. This lesson builds the full pipeline: PDF ingestion, chunking, embedding,
vector retrieval, and generation.

## What this teaches

- **The ingestion chain.** PDF → text → overlapping chunks → embeddings →
  vector store. Each step is a design decision (chunk size, overlap strategy,
  embedding model).
- **Retrieval as a tool.** The `retrieve` function is literally a tool the
  generative model depends on. The prompt tells it to use *only* retrieved
  context, forcing it to stay grounded.
- **Routing within RAG.** The pipeline re-uses the routing pattern from lesson
  02: after retrieval, a cheap model decides whether a simple or complex LLM
  should formulate the answer.

## Files

| File | Purpose |
|------|---------|
| `functions.py` | Shared utilities (embed, chunk, retrieve, answer) |
| `example.py` | Standalone CLI that ties the full pipeline together |

## How to run

```powershell
python example.py --pdf path/to/document.pdf --question "your question"
```
