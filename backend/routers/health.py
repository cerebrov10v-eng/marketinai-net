"""Health check router."""
import os
from fastapi import APIRouter

router = APIRouter(tags=["health"])


def _stripe_configured() -> str:
    return "configured" if bool(os.getenv("STRIPE_SECRET_KEY", "")) else "missing"


@router.get("/health")
async def health():
    return {"status": "ok", "service": "marketinai-api"}


@router.get("/health/detailed")
async def health_detailed():
    return {
        "status": "ok",
        "service": "marketinai-api",
        "checks": {
            "api": "ok",
            "database": "ok",
            "stripe": _stripe_configured(),
        },
    }
