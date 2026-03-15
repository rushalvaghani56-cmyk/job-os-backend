"""AI Provider Management schemas — API Contract Section 4.8.

Defines request/response models for API key management, model config, and usage stats.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class APIKeyInfo(BaseModel):
    """Masked API key info returned by GET /ai/keys."""

    id: uuid.UUID
    provider: str
    status: str
    last_validated: datetime | None = None
    masked_key: str  # e.g., "sk-...abcd"
    created_at: datetime

    model_config = {"from_attributes": True}


class APIKeyCreate(BaseModel):
    """POST /ai/keys request body."""

    provider: str  # anthropic, openai, google
    api_key: str


class APIKeyValidation(BaseModel):
    """Response from POST /ai/keys/:id/validate."""

    valid: bool
    error: str | None = None


class ModelConfig(BaseModel):
    """AI model configuration per task type."""

    task: str
    provider: str
    model: str
    max_tokens: int | None = None


class ModelConfigUpdate(BaseModel):
    """PUT /ai/models request body."""

    task_model_map: dict[str, dict]


class UsageStats(BaseModel):
    """AI usage statistics — GET /ai/usage."""

    period: str
    total_tokens: int = 0
    total_cost: float = 0.0
    by_provider: dict = {}
    by_task: dict = {}
