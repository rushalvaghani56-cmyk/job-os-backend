"""Content generation service — AI-powered resume, cover letter, and answer generation.

Uses BYOK API keys to call AI providers for document generation.
Stores generated documents in R2 and creates Document records.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession


async def generate_resume(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID, profile_id: uuid.UUID, instructions: str | None = None) -> str:
    """Generate a tailored resume. Returns task_id for async tracking."""
    raise NotImplementedError


async def generate_cover_letter(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID, profile_id: uuid.UUID) -> str:
    """Generate a cover letter. Returns task_id for async tracking."""
    raise NotImplementedError


async def generate_answers(db: AsyncSession, user_id: uuid.UUID, job_id: uuid.UUID, questions: list[str]) -> str:
    """Generate answers to application questions. Returns task_id."""
    raise NotImplementedError


async def regenerate_document(db: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID, instructions: str) -> str:
    """Regenerate a document with new instructions. Returns task_id."""
    raise NotImplementedError
