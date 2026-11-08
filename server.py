"""Vercel ASGI entrypoint. Configuration is required before importing."""
from app.main import create_app
app = create_app()
