"""Vercel serverless entry point — wraps FastAPI via Mangum."""

from mangum import Mangum
from src.web.app import create_app

app = create_app()
handler = Mangum(app, lifespan="off")
