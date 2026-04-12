# Acme Media — Recommendation Engine

> Python 3.11 / FastAPI · PyTorch · Redis 7 · PostgreSQL 15

## Overview

Personalized content recommendation service powered by collaborative filtering and deep learning. Serves real-time recommendations for home feeds, watch-next, and trending content with A/B testing support.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/recommendations/{userId}?context=home` | Home feed recommendations |
| GET | `/api/v1/recommendations/{userId}?context=watch-next&currentTitle={id}` | Watch-next suggestions |
| GET | `/api/v1/recommendations/trending` | Trending content |

## Architecture

```
┌──────────────────────────────────┐
│        FastAPI Application       │
│  ┌──────────────────────────┐  │
│  │ Content Recommender (PyTorch)│  │
│  └───────────┬──────────────┘  │
│              │                    │
│  ┌───────────▼──────────────┐  │
│  │   Redis Feature Store        │  │
│  └──────────────────────────┘  │
│  ┌────────────┐ ┌───────────┐  │
│  │ A/B Testing │ │ Trending  │  │
│  │  Service    │ │  Service  │  │
│  └────────────┘ └───────────┘  │
└──────────────────────────────────┘
```

## Running

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Docker

```bash
docker build -t acme-recommendation-engine .
docker run -p 8000:8000 acme-recommendation-engine
```
