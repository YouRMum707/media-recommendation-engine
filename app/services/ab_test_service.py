"""A/B test routing service."""

import hashlib

from app.config import settings


class ABTestService:
    """Deterministic A/B test routing based on user ID hashing."""

    async def get_variant(self, user_id: str, test_id: str) -> str | None:
        """Determine which A/B test variant a user should see."""
        if not settings.ab_test_enabled:
            return None

        # Deterministic hash-based assignment ensures consistent variant
        hash_input = f"{user_id}:{test_id}"
        hash_value = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16)
        bucket = hash_value % 100

        # Simple 50/50 split for now
        # In production, read from PostgreSQL ab_tests table
        if bucket < 50:
            return "control"
        else:
            return "variant-b"
