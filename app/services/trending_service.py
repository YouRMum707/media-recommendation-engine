"""Trending content calculation service."""

from redis.asyncio import Redis

from app.config import settings
from app.models.recommendation import TrendingItem


class TrendingService:
    """Calculates trending content based on view velocity and engagement."""

    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    async def get_trending(
        self, limit: int = 10, category: str | None = None
    ) -> list[TrendingItem]:
        """Retrieve trending content from the cached trending set."""
        cache_key = f"trending:{category or 'all'}"

        # Try cache first
        cached = await self.redis.get(cache_key)
        if cached:
            import json
            data = json.loads(cached)
            return [TrendingItem(**item) for item in data[:limit]]

        # Calculate from sorted set of view counts
        trending_key = f"views:{settings.trending_window_hours}h:{category or 'all'}"
        results = await self.redis.zrevrange(trending_key, 0, limit - 1, withscores=True)

        items = []
        for title_id, score in results:
            # Fetch title metadata from cache
            meta = await self.redis.hgetall(f"title:meta:{title_id}")
            items.append(
                TrendingItem(
                    title_id=title_id,
                    title=meta.get("title", f"Title {title_id}"),
                    trend_score=float(score),
                    views_24h=int(score),
                    thumbnail_url=meta.get("thumbnail_url", ""),
                    content_type=meta.get("content_type", "movie"),
                    category=category,
                )
            )

        # Cache results
        if items:
            import json
            await self.redis.setex(
                cache_key,
                settings.trending_cache_ttl,
                json.dumps([item.model_dump() for item in items]),
            )

        return items

    async def record_view(self, title_id: str, category: str | None = None) -> None:
        """Record a view event for trending calculation."""
        trending_key = f"views:{settings.trending_window_hours}h:all"
        await self.redis.zincrby(trending_key, 1, title_id)

        if category:
            cat_key = f"views:{settings.trending_window_hours}h:{category}"
            await self.redis.zincrby(cat_key, 1, title_id)
