"""ChipsTalk backend FastAPI application entry point."""

from fastapi import FastAPI

from app.api import health

app = FastAPI(title="ChipsTalk API")

app.include_router(health.router)
