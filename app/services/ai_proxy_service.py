"""AI proxy service — manages BYOK API keys and proxies requests to AI providers.

Handles key encryption/decryption, validation, model configuration,
and usage tracking per API Contract Section 4.8.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import APIKey


async def list_api_keys(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    """List all API keys for a user (masked, never expose plaintext)."""
    raise NotImplementedError


async def add_api_key(db: AsyncSession, user_id: uuid.UUID, provider: str, plaintext_key: str) -> APIKey:
    """Encrypt and store a new API key using AES-256-GCM per-user derived key."""
    raise NotImplementedError


async def delete_api_key(db: AsyncSession, user_id: uuid.UUID, key_id: uuid.UUID) -> None:
    """Delete an API key."""
    raise NotImplementedError


async def validate_api_key(db: AsyncSession, user_id: uuid.UUID, key_id: uuid.UUID) -> dict:
    """Decrypt and validate an API key by making a test call to the provider."""
    raise NotImplementedError


async def get_model_config(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    """Get AI model configuration per task type."""
    raise NotImplementedError


async def update_model_config(db: AsyncSession, user_id: uuid.UUID, task_model_map: dict) -> list[dict]:
    """Update AI model configuration."""
    raise NotImplementedError


async def get_usage_stats(db: AsyncSession, user_id: uuid.UUID, period: str) -> dict:
    """Get AI usage statistics for a period."""
    raise NotImplementedError
