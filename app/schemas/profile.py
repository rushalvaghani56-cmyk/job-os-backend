"""Profile schemas — API Contract Section 4.2.

Defines request/response models for profile CRUD, cloning, and completeness.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    """Create a new profile. Required: name, target_role."""

    name: str = Field(..., max_length=255)
    target_role: str = Field(..., max_length=255)
    target_seniority: str | None = None
    target_employment_types: list[str] | None = None
    target_locations: list[str] | None = None
    negative_locations: list[str] | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    years_experience: int | None = None
    current_title: str | None = None


class ProfileUpdate(BaseModel):
    """Update an existing profile. All fields optional."""

    name: str | None = None
    target_role: str | None = None
    target_seniority: str | None = None
    target_employment_types: list[str] | None = None
    target_locations: list[str] | None = None
    negative_locations: list[str] | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    years_experience: int | None = None
    current_title: str | None = None
    is_active: bool | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None
    bio_snippet: str | None = None
    ai_instructions: str | None = None
    scoring_weights: dict | None = None
    automation_config: dict | None = None
    discovery_config: dict | None = None
    dream_companies: list[str] | None = None
    blacklist: list[str] | None = None


class ProfileResponse(BaseModel):
    """Full profile representation returned by API."""

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    target_role: str
    target_seniority: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    completeness_pct: int = 0
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProfileCompleteness(BaseModel):
    """Profile completeness check result."""

    pct: int
    missing_items: list[str]


class CloneRequest(BaseModel):
    """Request body for POST /profiles/:id/clone."""

    name: str
    data_types: list[str] = Field(default_factory=list)
