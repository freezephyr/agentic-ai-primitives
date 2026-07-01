# LLM-as-Judge for RAG Evaluation

Evaluating a RAG pipeline is harder than building one. This lesson uses a
second LLM to score the first LLM's answers against expected ground truth.

## What this teaches

- **Automated grading with an LLM judge.** A `judge_prompt_generator` formats
  the question, expected answer, and actual answer into a scoring prompt that
  returns structured JSON (`{"test_id": N, "score": N}`).
- **Quantifying RAG quality.** Scores are averaged across test cases; any score
  below 3 / 5 is flagged as a failure. This gives a single number to track
  across pipeline changes.
- **Separation of concerns.** The evaluation logic (`example.py`) imports from
  the pipeline it tests (`03-rag-pipeline/functions.py`). The RAG code never
  knows it's being evaluated.

## How to run

```powershell
python example.py
```

The script runs a predefined set of questions (ownership, revenue, founder)
against a PDF and prints the average score along with any failing tests.
