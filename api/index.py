"""Vercel serverless entry point — exports FastAPI ASGI app directly."""

from src.web.app import create_app

app = create_app()
