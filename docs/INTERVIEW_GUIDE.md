# Explain the project from what you actually did

## Accurate starting narrative

“I built and tested a portfolio knowledge-assistant prototype with AI coding assistance. It ingests text documents, retrieves relevant chunks, and returns source-backed answers. I reviewed the request flow and tested authorization boundaries. Local preview uses extractive search; Azure mode uses embedding and chat deployments. I can show which parts I tested locally and which cloud checks I completed.”

Only say “deployed” after you have a working independent URL and have tested it. Only say “used Azure AI” after successful real embedding and chat requests. Do not present this new project as evidence of past employment, past customer usage, or previous production scale. Do not claim Qdrant, Chroma, LangChain or Semantic Kernel experience from this implementation; they are not used here.

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

## STAR material you can develop after hands-on review

Situation: a portfolio prototype to explore searching internal documentation.
Task: build a demonstrable, access-controlled question-answer flow.
Action: describe your actual design reviews, changes, debugging and test execution.
Result: quote actual test outcomes, observed timings and a live URL only when verified. The package has no production traffic results.

## Resume alignment

The current resume lists Azure OpenAI, Semantic Kernel, LangChain, Qdrant/Chroma and 500+ daily requests. This new review build does not substantiate that whole statement. Keep prior work claims tied to evidence from that work; describe this implementation separately as a personal project. After deployment, use a precise bullet such as:

“Built a Python/FastAPI knowledge-assistant prototype with document ingestion, role-filtered vector retrieval, source citations, Azure OpenAI integration, and automated API tests; deployed on [actual host] after verifying the end-to-end flow.”

Edit that statement to match the mode and hosting you actually verified.
