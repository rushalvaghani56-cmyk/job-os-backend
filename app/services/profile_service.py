"""Profile service — CRUD, cloning, completeness calculation.

Implements business logic for profile management per API Contract Section 4.2.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile


async def list_profiles(db: AsyncSession, user_id: uuid.UUID) -> list[Profile]:
    """List all non-deleted profiles for a user."""
    raise NotImplementedError


async def create_profile(db: AsyncSession, user_id: uuid.UUID, data: dict) -> Profile:
    """Create a new profile and compute initial completeness."""
    raise NotImplementedError


async def get_profile(db: AsyncSession, user_id: uuid.UUID, profile_id: uuid.UUID) -> Profile | None:
    """Get a profile by ID, enforcing user ownership."""
    raise NotImplementedError


async def update_profile(db: AsyncSession, user_id: uuid.UUID, profile_id: uuid.UUID, data: dict) -> Profile:
    """Update a profile and recompute completeness."""
    raise NotImplementedError


async def delete_profile(db: AsyncSession, user_id: uuid.UUID, profile_id: uuid.UUID) -> None:
    """Soft-delete a profile."""
    raise NotImplementedError


async def clone_profile(db: AsyncSession, user_id: uuid.UUID, profile_id: uuid.UUID, name: str, data_types: list[str]) -> Profile:
    """Clone a profile, optionally copying only selected data types."""
    raise NotImplementedError


async def activate_profile(db: AsyncSession, user_id: uuid.UUID, profile_id: uuid.UUID) -> Profile:
    """Set a profile as active, deactivating all others."""
    raise NotImplementedError


async def compute_completeness(profile: Profile) -> tuple[int, list[str]]:
    """Compute profile completeness percentage and list of missing items."""
    raise NotImplementedError
