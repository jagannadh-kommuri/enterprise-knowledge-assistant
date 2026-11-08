# Architecture — RC1

## System flow

Administrator → authenticated API → validated text/Markdown → overlapping chunks → Azure embeddings (or explicitly labeled local token-hash vectors) → SQL transaction with document visibility and vectors.

Question → hashed session lookup → shared SQL rate counter → query embedding → select only role-visible chunks → exact cosine scan → top supporting chunks → versioned grounding prompt → Azure chat completion (or extractive answer) → citation-range validation → answer with source excerpts and measured metadata.

No evidence bypasses generation. The model receives only authorized excerpts. Document contents and questions are not printed in the question metadata logs.

## Persistence and deployment

SQLite supports local review. The PostgreSQL adapter uses parameterized psycopg queries and SQL transactions. Sessions store a hash of a random opaque token, expiry, role and credential fingerprint. Password rotation invalidates sessions. Logout removes the persisted record. Rate counters use atomic upsert/returning queries with fixed one-minute windows across instances.

The Vercel entrypoint exports the FastAPI application. It requires DATABASE_URL and an initialized database; writable local files and process-local sessions are not used there. A separate initialization script creates tables before deployment. PostgreSQL connectivity, schema compatibility on the actual host and real Azure calls still require environment-backed integration checks.

## Interface

The full backend and hosted interface review share the same HTML/CSS/application JavaScript. The review substitutes a browser-local API adapter and REVIEW=true config. It is a UI simulation, not an auth/security test or a deployed Python service. Do not include that review adapter in a production server configuration.

## Tradeoffs

- Exact SQL-stored vector scan is simple and explainable but O(chunks × dimensions), not an ANN/vector database deployment.
- A direct Azure REST adapter keeps request flow visible. Qdrant/Chroma, LangChain and Semantic Kernel are not included.
- Two shared role passwords are suitable for a bounded portfolio demonstration, not employee SSO or per-user audit identity.
- Text/Markdown only; no PDF, OCR, virus scanner or background ingestion pipeline.
- Citation-range checks do not establish entailment; prompt instruction isolation does not guarantee injection immunity.
- Usage records count successful reported tokens; unavailable usage from failed calls and ingestion are excluded from question totals.
- The workspace is limited to 100 documents. Schema migrations, backups, retention, operational alerts and per-user cost budgets need further work before business use.

## Next meaningful validation

Run the PostgreSQL test with a disposable test database. Complete Azure end-to-end calls. Deploy the exact reviewed commit, perform restart/session checks, and test real mobile browsers. Evaluate retrieval recall and citation support on a labeled question set before making quality or capacity claims.
