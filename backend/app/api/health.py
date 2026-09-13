"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: returns 200 as soon as the API process is up."""
    return {"status": "ok"}
