# Vercel deployment — release candidate 1

The interface review is temporary and browser-local. This guide deploys the real FastAPI backend independently, with no ChatGPT authentication.

## 1. Review, then upload the code

After owner review, create a private `enterprise-knowledge-assistant` repository under `jagannadh-kommuri`. Upload this folder's contents at the repository root. Do not upload `.env`, `.venv/`, `data/`, caches, databases, credentials or personal documents. The owner authorized private GitHub upload. Public release remains gated on live acceptance testing.

## 2. Provision PostgreSQL

Create an empty dedicated managed PostgreSQL database using your preferred provider. Obtain its connection URL with TLS enabled (usually `sslmode=require` or stronger). Use a database account limited to this app. Keep separate databases for Vercel preview and production environments. Check the provider's current pricing before provisioning a paid resource.

The app stores document chunks, embeddings, sessions, metrics and request limits in SQL. SQLite remains supported for local review; Vercel explicitly requires PostgreSQL. Use an appropriate pooled URL from your provider when running serverless functions.

## 3. Configure the environment locally for initialization

Copy `.env.example` to `.env` and edit it locally. Fill these values:

| Variable | Required value |
|---|---|
| ADMIN_PASSWORD | Unique random password, at least 16 characters |
| READER_PASSWORD | Different unique password, at least 16 characters; optional |
| DATABASE_URL | PostgreSQL URL with TLS |
| AI_MODE | `azure` for actual AI, or `preview` for labeled extractive mode |
| COOKIE_SECURE | `true` for HTTPS hosting |
| PUBLIC_ORIGIN | Exact final origin, e.g. `https://your-project.vercel.app`; leave blank until known |
| AZURE_OPENAI_ENDPOINT | Azure resource root URL, only for azure mode |
| AZURE_OPENAI_API_KEY | Azure key, only for azure mode |
| AZURE_OPENAI_CHAT_DEPLOYMENT | Your actual chat deployment name, only for azure mode |
| AZURE_OPENAI_EMBEDDING_DEPLOYMENT | Your actual embedding deployment name, only for azure mode |

The Azure endpoint is `https://YOUR-RESOURCE.openai.azure.com`, without `/openai/v1`. Use a chat-completions-compatible deployment. Keys stay on the server. Never paste them into the app or GitHub.

Run:

```bash
python scripts/init_db.py
```

This loads the local `.env` safely and initializes tables with the configured embedding identity. It does not make a paid Azure model call. Initialize the database before Vercel deploys the app. The Vercel runtime checks the initialized database instead of performing schema changes on every cold start.

Changing embedding provider/model requires a fresh index and re-ingestion. Do not overwrite preview vectors with a different model.

## 4. Verify actual PostgreSQL

Set `TEST_DATABASE_URL` to a dedicated test database URL in your terminal environment, then run:

```bash
python -m pytest -q
```

The PostgreSQL integration test creates a disposable schema with a random name, verifies ingestion/retrieval, sessions across app instances and reader visibility, then removes that schema. If no test URL is supplied, it is explicitly skipped. A skipped test is not evidence of working PostgreSQL connectivity.

## 5. Import the repository into Vercel

1. Open https://vercel.com/new and connect the GitHub repository.
2. Use the repository root directory. Vercel should recognize **FastAPI**, not Vite.
3. Keep the framework defaults; there is no npm build or `dist` output directory for this backend project.
4. The supported entrypoint is specified as `server:app` in `pyproject.toml`.
5. Add the values above to Vercel's environment settings. Do not set `DATABASE_PATH` or `INIT_SCHEMA` for Vercel.
6. Set Python 3.12 if the dashboard offers a version selector. `pyproject.toml` also constrains it.
7. Deploy. The configuration allows up to 300 seconds for the function; confirm the chosen plan supports the desired duration. Model timeout/retries can increase latency and billed usage.
8. When Vercel supplies the address, set `PUBLIC_ORIGIN` to that exact origin and redeploy. Update it when attaching a custom domain. One canonical origin is supported at a time.

## 6. Live acceptance checklist

- [ ] `/health` returns `{"status":"ok"}`.
- [ ] App sign-in uses the workspace password without ChatGPT login.
- [ ] The mode badge matches the intended mode.
- [ ] Upload two fictional documents; ask relevant questions; inspect citations.
- [ ] Confirm real Azure token usage on a successful AI question.
- [ ] Reader cannot list/retrieve admin-only content or call mutation/metrics endpoints.
- [ ] Sign in, redeploy/restart, and confirm session plus documents persist.
- [ ] Logout invalidates the session; password change revokes the role's sessions.
- [ ] Test real iOS Safari, Android Chrome, and desktop browsers.
- [ ] Check loading, empty, invalid-input and provider-error states.
- [ ] Confirm `.env` and credentials are absent from GitHub and browser network payloads.

Do not describe the full app as verified live until these checks pass. Backend integration and cloud deployment remain unverified in the delivered release candidate.

## Alternative Docker hosting

The Dockerfile remains usable on a container host. Configure the same environment, preferably PostgreSQL for shared storage. For single-instance SQLite hosting, mount durable storage at `/data`. Use HTTPS with secure cookies. Do not expose a proxy-trusting container directly to untrusted traffic. The Docker image has not been built in this environment.

## Reference docs

- https://vercel.com/docs/frameworks/backend/fastapi
- https://vercel.com/docs/functions/runtimes/python
- https://learn.microsoft.com/en-us/rest/api/microsoft-foundry/azureopenai/chat
- https://learn.microsoft.com/en-us/rest/api/microsoft-foundry/azureopenai/embeddings
