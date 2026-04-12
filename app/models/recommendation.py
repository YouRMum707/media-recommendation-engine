"""Pydantic models for recommendation API responses."""

from pydantic import BaseModel, Field


class RecommendedItem(BaseModel):
    """A single recommended content item."""

    title_id: str
    title: str
    score: float = Field(ge=0.0, le=1.0, description="Relevance score")
    reason: str = Field(description="Why this was recommended")
    thumbnail_url: str
    content_type: str  # movie, series, article, video
    genre: str | None = None
    duration: int | None = None  # seconds


class RecommendationResponse(BaseModel):
    """Response for personalized recommendations."""

    user_id: str
    context: str
    recommendations: list[RecommendedItem]
    model_version: str


class TrendingItem(BaseModel):
    """A single trending content item."""

    title_id: str
    title: str
    trend_score: float
    views_24h: int
    thumbnail_url: str
    content_type: str
    category: str | None = None


class TrendingResponse(BaseModel):
    """Response for trending content."""

    items: list[TrendingItem]
    window_hours: int
