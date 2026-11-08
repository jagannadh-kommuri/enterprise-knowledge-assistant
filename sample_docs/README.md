# Upload these test documents

All content is fictional. Upload .md files individually using Add document. The app does not currently parse PDF, Word, screenshots, or ZIP files.

1. incident-response.md — title Incident response handbook; visibility Team.
2. access-policy.md — title Access and document policy; visibility Team.
3. onboarding.md — title Engineering onboarding; visibility Team.
4. restricted-launch.md — title Restricted launch plan; visibility Administrators only. The visibility setting, not the filename or document text, enforces backend access.

Do NOT upload this README or the test guide: they contain expected answers and would contaminate the test. Use a clean test workspace; existing sample documents can duplicate sources.

Test questions and expected facts:

| Question | Expected fact | Source |
|---|---|---|
| What are the requirements for an incident rollback? | Last known healthy release, recorded incident ID, incident commander approval | Incident response handbook |
| How long should we verify health after rollback? | Ten minutes; API errors, latency and database connection health | Incident response handbook |
| When is an incident postmortem due? | Within three business days | Incident response handbook |
| How do new employees request application access? | Service desk; manager approval; least privileged role | Access and document policy |
| When does production access expire? | Thirty days unless renewed | Access and document policy |
| What should a new engineer do during the first week? | Run app locally, read incident handbook, documentation PR reviewed by mentor | Engineering onboarding |
| What is the violetmonsoon launch review date? (admin) | December 10, 2026 | Restricted launch plan |
| What is the violetmonsoon launch review date? (reader) | No restricted excerpt, date or codename disclosure in generated answer | No restricted source |
| What is the cafeteria lunch menu? | Insufficient supporting evidence; no invented menu | None |

For each supported question, open the citation and verify its document and excerpt. Extractive preview can quote longer passages; live AI may paraphrase. A relevant citation alone does not prove every claim is supported.

Also test: blank input rejected, upload appears in library, filter by title, logout, reader cannot upload/delete, deletion removes retrieval, refresh preserves documents. In the hosted UI preview, roles are only simulated. Repeat authorization tests against the Python backend. Repeat persistence after a hosted redeploy.

Release gate: local tests, real PostgreSQL integration, live Azure embeddings and chat, failure handling, hosted persistence, real phone browsers, and owner review must pass before public release. Record date, environment, actual result and PASS/FAIL for each case. Do not mark an unrun test PASS.
