"""AI Provider Management API endpoints — API Contract Section 4.8.

7 endpoints: list keys, add key, delete key, validate key, list models, update models, usage.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import (
    APIKeyCreate,
    APIKeyInfo,
    APIKeyValidation,
    ModelConfig,
    ModelConfigUpdate,
    UsageStats,
)
from app.schemas.common import DataResponse, SuccessResponse

router = APIRouter(prefix="/ai")


@router.get("/keys", response_model=DataResponse[list[APIKeyInfo]])
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[list[APIKeyInfo]]:
    """List all API keys (masked) for the current user."""
    raise NotImplementedError


@router.post("/keys", status_code=status.HTTP_201_CREATED, response_model=DataResponse[APIKeyInfo])
async def add_api_key(
    body: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[APIKeyInfo]:
    """Add and encrypt a new API key."""
    raise NotImplementedError


@router.delete("/keys/{key_id}", response_model=SuccessResponse)
async def delete_api_key(
    key_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Delete an API key."""
    raise NotImplementedError


@router.post("/keys/{key_id}/validate", response_model=APIKeyValidation)
async def validate_api_key(
    key_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> APIKeyValidation:
    """Validate an API key by making a test call to the provider."""
    raise NotImplementedError


@router.get("/models", response_model=DataResponse[list[ModelConfig]])
async def list_models(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[list[ModelConfig]]:
    """List configured AI models per task type."""
    raise NotImplementedError


@router.put("/models", response_model=DataResponse[list[ModelConfig]])
async def update_models(
    body: ModelConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[list[ModelConfig]]:
    """Update AI model configuration."""
    raise NotImplementedError


@router.get("/usage", response_model=DataResponse[UsageStats])
async def get_usage(
    period: str = Query(default="30d"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[UsageStats]:
    """Get AI usage statistics for a period."""
    raise NotImplementedError
