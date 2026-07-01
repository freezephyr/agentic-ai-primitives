
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from litellm import completion, embedding
from pypdf import PdfReader

load_dotenv()

logger = logging.getLogger(__name__)


# --- Model selection -------------------------------------------------------

MODELS_BY_INTENT = {
    "embedding": "bedrock/amazon.titan-embed-text-v2:0",
    "routing": "bedrock/amazon.nova-micro-v1:0",
    "simple": "bedrock/amazon.nova-micro-v1:0",
    "tool": "bedrock/qwen.qwen3-coder-next",
    "complex": "bedrock/amazon.nova-pro-v1:0",
}


def model_for(intent: str) -> str:
    try:
        return MODELS_BY_INTENT[intent]
    except KeyError:
        raise ValueError(
            f"Unknown intent {intent!r}; expected one of {list(MODELS_BY_INTENT)}"
        )


# --- LLM + embeddings ------------------------------------------------------

def run_inference(messages, intent: str = "simple", tools=None):
    """Run a chat completion. Returns (content, tool_calls)."""
    kwargs = {"model": model_for(intent), "messages": messages}
    if tools is not None:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    message = completion(**kwargs).choices[0].message
    return message.content, getattr(message, "tool_calls", None)


def embed_texts(texts: list[str], intent: str = "embedding") -> list[list[float]]:
    """Embed a batch of texts; returns one vector per input, in order."""
    response = embedding(model=model_for(intent), input=texts)
    return [item["embedding"] for item in response.data]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]


def route_intent(prompt: str, tools=None) -> str:
    """Classify a prompt as 'simple', 'tool', or 'complex' (falls back to 'simple')."""
    instruction = (
        "Evaluate the user prompt and respond with exactly one word: "
        "'simple', 'tool', or 'complex'. "
        "Use 'simple' if a small model can answer it, "
        "'tool' if it can be solved with the provided tools, "
        "'complex' if a larger model is needed.\n\n"
        f"User prompt: {prompt}\n"
    )
    if tools is not None:
        instruction += f"Tools: {tools}\n"
    content, _ = run_inference(
        [{"role": "user", "content": instruction}], intent="routing"
    )
    intent = (content or "").strip().lower()
    return intent if intent in {"simple", "tool", "complex"} else "simple"


# --- Document ingestion ----------------------------------------------------

@dataclass
class Document:
    name: str
    path: str
    pages: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(self.pages)


def load_pdf(pdf_path: str) -> Document:
    """Read a PDF into a Document, one entry per page."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    doc = Document(name=path.name, path=str(path))
    for page in PdfReader(str(path)).pages:
        doc.pages.append((page.extract_text() or "").strip())
    return doc


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping character windows."""
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size")
    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text) - chunk_size + 1, step)
    ]
    if (len(text) - chunk_size) % step:
        chunks.append(text[-chunk_size:])
    return chunks


# --- Vector store ----------------------------------------------------------

def build_collection(name: str, chunks: list[str], source: str):
    """Embed chunks and load them into a Chroma collection."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(name)
    embeddings = embed_texts(chunks)
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source} for _ in chunks],
    )
    return collection


def retrieve(collection, question: str, n_results: int = 3) -> list[str]:
    result = collection.query(
        query_embeddings=[embed_query(question)], n_results=n_results
    )
    return result["documents"][0]


# --- RAG orchestration -----------------------------------------------------

def answer_question(collection, question: str, n_results: int = 3) -> str:
    passages = retrieve(collection, question, n_results)
    context = "\n".join(f"[{i + 1}] {p}" for i, p in enumerate(passages))
    prompt = (
        "Answer the user's question using ONLY the retrieved context below. "
        "If the context does not contain the answer, say so.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n{context}"
    )
    intent = route_intent(prompt)
    logger.info("Routed question to '%s' model", intent)
    content, _ = run_inference(
        [{"role": "user", "content": prompt}], intent=intent
    )
    return content or ""
