# Atlas project walkthrough

Atlas is a personal knowledge workspace maintained by Jagannadh Kommuri. It indexes uploaded documents, retrieves relevant excerpts, and cites the physical page for PDFs. The live workspace uses extractive search. Azure OpenAI is an optional integration for embeddings and generated answers.

## A five-minute demo

1. Sign in as administrator; show the mode badge.
2. Upload the fictional incident handbook.
3. Ask about rollback and inspect the source excerpt.
4. Ask an unrelated question; show the evidence-insufficiency response.
5. Add an administrator-only document and switch to reader to show the boundary.
6. Return as admin, show measured usage and explain token/latency limits.

## Concepts to practice

- **RAG:** retrieve relevant source passages before asking a model to answer; it does not retrain the model.
- **Embedding:** a numeric representation used for similarity. Preview token hashing is not semantic embedding.
- **Chunking:** split a long document so retrieval can return small, relevant units; overlap preserves nearby context but costs storage and tokens.
- **Cosine similarity:** compare vector direction; normalize with vector magnitudes. A large score is not a truth guarantee.
- **Hallucination handling:** limit context, require citations, refuse when retrieval is insufficient, validate citation ranges, and verify claims against sources.
- **Prompt injection:** documents are data, not commands. The prompt says so; no external-action tools exist. This is risk reduction, not a proof of immunity.
- **Security:** backend auth and role checks, pre-retrieval filtering, HTTP-only cookies, hashed SQL-backed sessions, shared SQL rate counters, same-origin writes, CSP, and safe DOM rendering.
- **Scaling:** current exact scan is linear in stored chunks; a vector database and shared sessions/data are needed for larger workloads.
- **Retries:** capped retries with backoff on provider trouble; they may duplicate billable calls, so a real system needs stronger budgets and observability.
- **Evaluation:** measure retrieval recall@k, citation correctness, no-answer behavior, role isolation, latency percentiles, and cost per query on representative examples.

## Discuss the implementation

Explain the PDF ingestion flow, how page numbers are preserved, and how the backend filters documents by role before retrieval. Use verified test results and a working deployment URL when describing the project. Describe any optional model integration according to the environment you tested.
