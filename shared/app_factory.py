import os
from typing import Callable, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def _cors_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_service_app(service_name: str, router: Optional[Callable] = None, *, health_service_name: Optional[str] = None):
    """Create a consistent microservice app with shared security defaults.

    The router argument is expected to be a FastAPI router instance or callable that
    accepts a service object and returns the router. This keeps the app factory
    reusable across all microservices while preserving each service-specific API.
    """
    app = FastAPI(title=f"ms-{service_name}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": health_service_name or service_name}

    if router is not None:
        app.include_router(router)

    return app
