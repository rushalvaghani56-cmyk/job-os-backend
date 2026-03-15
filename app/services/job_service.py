"""Job service — CRUD, status management, search, manual creation.

Implements business logic for job management per API Contract Section 4.3.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job


async def list_jobs(
    db: AsyncSession, user_id: uuid.UUID, cursor: str | None, limit: int,
    sort: str | None, filters: dict,
) -> tuple[list[Job], str | None, bool]:
    """List jobs with cursor pagination and filters. Returns (jobs, next_cursor, has_more)."""
    raise NotImplementedError


async def get_job(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID) -> Job | None:
    """Get a job by ID, enforcing user ownership."""
    raise NotImplementedError


async def create_job_manual(db: AsyncSession, user_id: uuid.UUID, url: str | None, raw_text: str | None, profile_id: uuid.UUID) -> Job:
    """Create a job from a URL or raw text, parsing and normalizing fields."""
    raise NotImplementedError


async def update_job_status(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID, status: str) -> Job:
    """Update a job's status."""
    raise NotImplementedError


async def bookmark_job(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID) -> Job:
    """Set job status to bookmarked."""
    raise NotImplementedError


async def skip_job(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID) -> Job:
    """Set job status to skipped."""
    raise NotImplementedError


async def search_jobs(db: AsyncSession, user_id: uuid.UUID, query: str, limit: int) -> list[Job]:
    """Full-text search using tsvector index."""
    raise NotImplementedError
