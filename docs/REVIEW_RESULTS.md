# Release evidence — RC1, 2026-11-07

## Passed

- **17 backend tests**: ingestion/retrieval/deletion, reader role boundaries, no-evidence handling, authentication, same-origin checks, login rate limiting, simulated Azure contract/citation validation, provider failure recording and index identity protection.
- Additional tests cover sessions across app instances, cross-instance logout, password-change revocation, shared rate limits, hashed token storage, session expiry, Vercel storage guards, and production UI configuration.
- **6 browser-preview adapter tests**: review role selection, seeded retrieval/citations, document ingestion/persistence/retrieval/deletion, simulated reader visibility, no evidence, invalid questions and actual activity counters.
- JavaScript syntax and Python compilation checks passed.
- Actual Uvicorn **server:app** HTTP smoke check passed: interface/assets, sign-in, sample document ingestion, retrieval/citations, and session/document persistence across a complete process restart.
- Browser interaction QA: redesigned research desk, sample question, evidence panel, document dialog submission, title filtering, mobile navigation drawer and library navigation.
- Layout inspection at desktop and 390/412 CSS-pixel widths. A phone text-spacing issue was fixed during inspection.

## Not verified

- **1 PostgreSQL integration test skipped**: no TEST_DATABASE_URL supplied. PostgreSQL connectivity/schema behavior must be tested using a real dedicated database before production signoff.
- Real Azure embeddings/chat calls: no credentials supplied; contract tests use simulated responses.
- Vercel deployment/build and Docker image build: not performed.
- Physical iOS Safari/Android Chrome testing: not performed. Width previews are not OS/browser emulation.
- Load/capacity, traffic, 500+ daily requests, latency improvements, SLA, enterprise SSO or compliance: not claimed.

## Review package versus hosted review

The full app uses FastAPI, real backend access checks and database persistence. The hosted review uses the exact same frontend with browser-local API/config adapters. It is labeled as a UI preview. Review role controls do not provide security. No GitHub upload has been performed.

This is a reviewed **release candidate**, not a claim of fully verified production deployment. See DEPLOYMENT.md for cloud acceptance checks.
