# Atlas — Enterprise Knowledge Assistant

**Release candidate 1 · ready for interface review and configured for a Vercel deployment.**

A personal project by Jagannadh Kommuri. Atlas is a Python/FastAPI application with a custom responsive research interface, document ingestion, role-filtered retrieval, source-linked answers and measured usage. The same interface is used by the temporary browser-local review and by this full backend; only the API adapter and review configuration differ.

## Current state

| Component | State |
|---|---|
| Custom research desk, library, source panel, upload/delete dialogs | Implemented |
| Authentication, reader/admin permissions, vector retrieval, metrics | Implemented and tested locally |
| Persistent shared sessions and request limits | Implemented in SQL; tested across local app instances |
| PostgreSQL deployment adapter, Vercel entrypoint/config | Included; live PostgreSQL/Vercel verification pending |
| Azure embedding/chat integration | Included; provider-contract tests use simulated responses; real Azure calls pending |
| Qdrant, Chroma, LangChain, Semantic Kernel | Not implemented in this release |
| GitHub | Private testing repository; public release pending |
| Independent cloud deployment | Pending live PostgreSQL and Azure setup |

Do not describe the preview as a live AI deployment. No traffic, 500+ daily requests, SLA, or performance-improvement claims are made.

## Run the complete application locally

Use Python 3.12. Open a terminal in this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_local.py
```

Windows: use `python` and `.venv\Scripts\activate` for the first two commands.

Open http://127.0.0.1:8000. First run creates `.env` with random admin and reader passwords. Open that local file and sign in with `ADMIN_PASSWORD`. Do not upload or share `.env`. The server is loopback-only. Stop it with Ctrl+C.

Open **Document library → Load fictional sample library**. Ask a sample question. Click its numbered citation to open the source excerpt. Test a reader login with `READER_PASSWORD` to check the real backend boundary. The browser review's role switch is only a simulation.

For a reproducible interface-only preview, run `python -m http.server 8080 --directory review-preview --bind 127.0.0.1` and open http://127.0.0.1:8080. This uses local browser storage and simulated roles. Deploy the repository root, not `review-preview/`, when deploying the backend.

## Connect actual AI

In `.env`, set `AI_MODE=azure`, your Azure resource root endpoint, API key, chat deployment and embedding deployment names. Use a new `DATABASE_PATH=./data/azure.sqlite3` for local AI review, or a fresh PostgreSQL database. Restart and re-upload documents. Azure mode fails closed if configuration is missing; it never silently falls back to preview.

`AI_MODE=preview` uses deterministic token-hash embeddings plus lexical overlap and returns source excerpts. It is not semantic search or generated AI. The UI labels the active mode.

## Deploy to Vercel

Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). The package includes `server.py`, `pyproject.toml`, `vercel.json`, a PostgreSQL adapter and an initialization command. **Do not deploy with a writable local SQLite file on Vercel.** The app rejects Vercel startup without `DATABASE_URL`.

Before calling it production-ready, configure a managed PostgreSQL database and Azure deployments, run the PostgreSQL integration test, deploy to Vercel, and complete the live acceptance checklist. Credentials and host deployment have not been supplied/tested here.

## Verification

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
node --check app/static/app.js
node --test tests/review.test.mjs
```

For real database verification, provide a dedicated `TEST_DATABASE_URL` and rerun pytest. The test creates and removes an isolated schema; it must not be pointed at an application database account without permission to create test schemas.

## Structure

- `app/main.py`: API, grounding prompt, Azure provider, retrieval and role checks
- `app/storage.py`: SQLite/PostgreSQL bridge
- `app/static/`: interface and HTTP API adapter; no frontend build step
- `server.py`: Vercel ASGI entrypoint
- `scripts/init_db.py`: deployment database initialization
- `tests/`: API and optional real PostgreSQL tests
- `sample_docs/`: fictional sample Markdown
- `docs/`: deployment guide, architecture, interview notes and release evidence

## Design and scope

The research desk keeps questions and findings in the main column and their supporting excerpts in a side panel. Mobile layouts use an accessible navigation toggle and stack the source panel beneath the answer. Real-device iOS Safari/Android Chrome checks remain part of owner review.

This is a bounded portfolio application: one shared workspace, two role passwords, one-hour opaque sessions stored as hashes, 100 text/Markdown documents maximum, exact vector scanning, and a versioned grounding prompt. No enterprise SSO, per-person permissions, multi-tenancy, PDF/OCR, background ingestion queue, distributed vector index, or compliance certification is claimed.

Changing a workspace password invalidates existing sessions for that role. Sessions, documents, metrics and request counters persist in the deployment database. Rate limits use fixed one-minute windows, not a rolling-window global capacity guarantee. Configure TLS on PostgreSQL and your host, protect environment secrets, and use fictional content for public demonstrations.

Citation-range validation does not prove factual entailment. Prompt isolation and absence of action tools reduce risk without proving prompt-injection immunity. Retrieval thresholds and chunk sizes are initial settings; evaluate relevance on representative questions before using real business material.

## Test documents
See [sample_docs/README.md](sample_docs/README.md) for upload instructions, visibility settings, questions and expected answers. Local tests: 21 passed, 1 PostgreSQL test skipped; 6 browser-adapter tests passed. Live Azure and cloud deployment are not verified.

## PDF page citations
See [PDF support and test status](docs/PDF_CITATIONS.md). Text-based PDFs now retain physical page numbers in source cards and copied references.
