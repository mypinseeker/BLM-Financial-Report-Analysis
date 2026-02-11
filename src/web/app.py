"""FastAPI application factory for the BLM Web App."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Load env vars — check multiple locations
_DB_ENV = Path(__file__).resolve().parent.parent / "database" / ".env"
if _DB_ENV.exists():
    load_dotenv(_DB_ENV)
load_dotenv()  # also load from cwd / .env

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app() -> FastAPI:
    app = FastAPI(
        title="BLM Financial Report Analysis",
        description="Telecom market analysis dashboard",
        version="1.0.0",
    )

    # Register API routers
    from src.web.routers import markets, operators, outputs, cloud, pages
    from src.web.routers import groups, analyze, data_extract
    app.include_router(markets.router)
    app.include_router(operators.router)
    app.include_router(outputs.router)
    app.include_router(cloud.router)
    app.include_router(groups.router)
    app.include_router(analyze.router)
    app.include_router(data_extract.router)
    app.include_router(pages.router)

    return app
