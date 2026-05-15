from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.observability import configure_logging, configure_sentry
from app.routers import alerts, auth, health, notifications, subscriptions


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)
    configure_sentry(settings)
    app = FastAPI(title="Thrifty API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(subscriptions.router)
    app.include_router(alerts.router)
    app.include_router(notifications.router)
    app.include_router(health.router)
    return app


app = create_app()
