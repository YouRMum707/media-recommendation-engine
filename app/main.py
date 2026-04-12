"""Acme Media Recommendation Engine — FastAPI application."""

from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup: connect to Redis feature store
    app.state.redis = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    yield
    # Shutdown: close connections
    await app.state.redis.close()


app = FastAPI(
    title="Acme Media Recommendation Engine",
    description="Personalized content recommendations powered by PyTorch",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(recommendations.router, prefix="/api/v1/recommendations")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
