"""Redis-backed feature store for ML model inference."""

import json

from redis.asyncio import Redis

from app.config import settings


class FeatureStore:
    """Manages user and title feature vectors in Redis for low-latency inference."""

    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    async def get_user_features(self, user_id: str) -> dict:
        """Retrieve user feature vector from the feature store."""
        data = await self.redis.get(f"features:user:{user_id}")
        if data:
            return json.loads(data)

        # Return default features for new/unknown users
        return {
            "embedding": [0.0] * 128,
            "watch_history_count": 0,
            "preferred_genres": [],
            "avg_watch_duration": 0,
            "tier": "free",
        }

    async def set_user_features(self, user_id: str, features: dict) -> None:
        """Store user feature vector in the feature store."""
        await self.redis.setex(
            f"features:user:{user_id}",
            settings.feature_store_ttl,
            json.dumps(features),
        )

    async def get_title_features(self, title_id: str) -> dict:
        """Retrieve title feature vector from the feature store."""
        data = await self.redis.get(f"features:title:{title_id}")
        if data:
            return json.loads(data)

        return {
            "embedding": [0.0] * 128,
            "genre": "unknown",
            "popularity_score": 0.5,
            "release_year": 2024,
        }

    async def set_title_features(self, title_id: str, features: dict) -> None:
        """Store title feature vector in the feature store."""
        await self.redis.setex(
            f"features:title:{title_id}",
            settings.feature_store_ttl,
            json.dumps(features),
        )
