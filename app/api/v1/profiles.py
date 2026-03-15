"""Profile API endpoints — API Contract Section 4.2.

8 endpoints: list, create, get, update, delete, clone, activate, completeness.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import DataResponse, SuccessResponse
from app.schemas.profile import (
    CloneRequest,
    ProfileCompleteness,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)

router = APIRouter(prefix="/profiles")


@router.get("", response_model=DataResponse[list[ProfileResponse]])
async def list_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[list[ProfileResponse]]:
    """List all profiles for the current user."""
    raise NotImplementedError


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DataResponse[ProfileResponse])
async def create_profile(
    body: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ProfileResponse]:
    """Create a new profile."""
    raise NotImplementedError


@router.get("/{profile_id}", response_model=DataResponse[ProfileResponse])
async def get_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ProfileResponse]:
    """Get a profile by ID."""
    raise NotImplementedError


@router.put("/{profile_id}", response_model=DataResponse[ProfileResponse])
async def update_profile(
    profile_id: uuid.UUID,
    body: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ProfileResponse]:
    """Update a profile."""
    raise NotImplementedError


@router.delete("/{profile_id}", response_model=SuccessResponse)
async def delete_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Soft-delete a profile."""
    raise NotImplementedError


@router.post("/{profile_id}/clone", status_code=status.HTTP_201_CREATED, response_model=DataResponse[ProfileResponse])
async def clone_profile(
    profile_id: uuid.UUID,
    body: CloneRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ProfileResponse]:
    """Clone a profile with selected data types."""
    raise NotImplementedError


@router.put("/{profile_id}/activate", response_model=DataResponse[ProfileResponse])
async def activate_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ProfileResponse]:
    """Set a profile as the active profile (deactivates others)."""
    raise NotImplementedError


@router.get("/{profile_id}/completeness", response_model=ProfileCompleteness)
async def get_completeness(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProfileCompleteness:
    """Calculate and return profile completeness percentage."""
    raise NotImplementedError
