"""A/B test configuration model."""

from pydantic import BaseModel, Field


class ABTestConfig(BaseModel):
    """Configuration for an A/B test experiment."""

    test_id: str
    name: str
    description: str = ""
    enabled: bool = True
    variants: list["ABVariant"]
    traffic_percentage: float = Field(ge=0.0, le=1.0, default=1.0)


class ABVariant(BaseModel):
    """A single variant within an A/B test."""

    variant_id: str
    name: str
    weight: float = Field(ge=0.0, le=1.0, description="Traffic weight for this variant")
    model_version: str | None = None
    parameters: dict[str, str | int | float | bool] = {}
