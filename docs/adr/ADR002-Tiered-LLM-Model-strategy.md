# ADR002-Tiered Foundation Model Strategy for Agentic workloads
Status: Accepted
Decider(s): Sahil M Principal Architect
Date: 2026-06-30
Supersedes: None# Architecture Decision Record: Tiered Foundation Model Strategy for Agentic RAG


## 1. Context and Problem Statement
We are building a production-grade Agentic workloads including RAG (Retrieval-Augmented Generation) system. Executing every phase of an agentic loop—such as classification, vector embedding generation, tool calling, and final synthesis—through a single monolith frontier model (e.g., Claude 3.5 Opus) is financially and operationally unsustainable. 

A single-model approach forces simple tasks (like routing a 10-word sentence) to incur massive token costs and high time-to-first-token (TTFT) latency overhead. To scale the system while maintaining sub-second user responsiveness and viable gross margins, we must decouple the workflow into discrete tasks and bind each task to a model optimized strictly for its specific cost-to-latency profile.

---

## 2. Decision Drivers
* **Latency Optimization:** Simple orchestration steps (classification, routing) must execute with <100ms processing times to prevent compounding delays across multi-turn loops.
* **Cost Efficiency (Token Economics):** High-volume, programmatic requests (embeddings and basic structural generation) must scale sub-linearly with user growth, protecting our target margin.
* **JSON Schema Enforcement:** High precision for structured tool execution to prevent invalid token payloads and costly retries.
* **Context Volume vs. Cost:** Deep context processing for final answer synthesis must balance long-context window support with reasonable per-token cost boundaries.

---

## 3. Considered Architectural Options
* **Option 1: Monolithic Frontier Routing** — Pass all pipeline steps to a single top-tier model.
* **Option 2: Tiered Optimization on Amazon Bedrock** — Route tasks dynamically across a spectrum of highly specialized, low-cost/low-latency models (Titan, Nova Micro, Qwen, Nova Pro).

---

## 4. Evaluation of Options

### Option 1: Monolithic Frontier Routing
* **Description:** Use a singular high-intelligence model for the entire agent pipeline.
* **Pros:** Minimal orchestration complexity; single SDK client.
* **Cons:** * **Cost Prohibitive:** Paying frontier prices $15.00 per million tokens for basic intent routing.
    * **Latency Bottleneck:** High TTFT on every sub-turn drastically hurts interactive user experience.

### Option 2: Tiered Optimization on Amazon Bedrock
* **Description:** Implement a strict multi-model topology mapping tasks directly to their lowest feasible cost and latency tier.
* **Pros:** Maximum control over our cost-per-inference metrics and pipeline execution time.
* **Cons:** Increased application logic to handle state across four distinct model endpoints.

---

## 5. The Decision: Tiered Model Selection Strategy
We chose **Option 2**. We are standardizing on a four-tier architecture on Amazon Bedrock using the matrix below, explicitly optimized for cost and latency bounds:

| Workflow Tier | Selected Model | Primary Task | Latency Profile | Cost Profile (Approx.) | Selection Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Embedding** | `amazon.titan-embed-text-v2` | Document vectorization & chunk indexing | Low (Parallelized batching) | **$0.02 per million tokens** | Lowest-cost enterprise embedder; 1024-dimension option optimizes downstream vector storage cost. |
| **2. Routing** | `amazon.nova-micro-v1` | Intent classification & triage | **Ultra-Low (Sub-150 ms)** | **$0.035 per million tokens** | Blazing-fast text-only model. Eliminates routing latency bottlenecks at fractions of a cent. |
| **3. Tool Execution** | `qwen` (Bedrock Marketplace) | JSON function-calling / schema binding | Moderate sub 500ms) | **Low to Moderate** | Outperforms larger models on function-calling accuracy, eliminating costly validation retries. |
| **4. Synthesis** | `amazon.nova-pro-v1` | Complex reasoning & multi-source RAG generation | Higher (Context dependent) | **High-tier capability at mid-tier pricing** | Provides the 300k long-context and multimodal logic required for final generation without the pricing premium of competitive frontier APIs. |
