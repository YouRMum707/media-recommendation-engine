"""Recommendation API endpoints."""

from fastapi import APIRouter, Depends, Query, Request

from app.models.recommendation import RecommendationResponse, TrendingResponse
from app.services.content_recommender import ContentRecommender
from app.services.trending_service import TrendingService
from app.services.ab_test_service import ABTestService
from app.services.feature_store import FeatureStore
from app.config import settings

router = APIRouter()


def get_feature_store(request: Request) -> FeatureStore:
    return FeatureStore(request.app.state.redis)


def get_recommender(feature_store: FeatureStore = Depends(get_feature_store)) -> ContentRecommender:
    return ContentRecommender(feature_store)


def get_trending_service(request: Request) -> TrendingService:
    return TrendingService(request.app.state.redis)


def get_ab_test_service() -> ABTestService:
    return ABTestService()


@router.get("/{user_id}", response_model=RecommendationResponse)
async def get_recommendations(
    user_id: str,
    context: str = Query("home", description="Recommendation context: home, watch-next, category"),
    current_title: str | None = Query(None, alias="currentTitle", description="Current title for watch-next"),
    limit: int = Query(settings.default_recommendations, ge=1, le=settings.max_recommendations),
    recommender: ContentRecommender = Depends(get_recommender),
    ab_service: ABTestService = Depends(get_ab_test_service),
):
    """Get personalized recommendations for a user."""
    # Determine A/B test variant
    variant = await ab_service.get_variant(user_id, "rec-model-v2")

    recommendations = await recommender.recommend(
        user_id=user_id,
        context=context,
        current_title_id=current_title,
        limit=limit,
        model_variant=variant,
    )

    return RecommendationResponse(
        user_id=user_id,
        context=context,
        recommendations=recommendations,
        model_version=variant or "v1",
    )


@router.get("/trending", response_model=TrendingResponse)
async def get_trending(
    limit: int = Query(10, ge=1, le=50),
    category: str | None = None,
    trending_service: TrendingService = Depends(get_trending_service),
):
    """Get trending content across the platform."""
    items = await trending_service.get_trending(limit=limit, category=category)
    return TrendingResponse(items=items, window_hours=settings.trending_window_hours)
