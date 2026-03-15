"""Review Queue service — approve, reject, regenerate review items.

Implements business logic for the human review queue per API Contract Section 4.6.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review_queue import ReviewQueue


async def list_review_items(
    db: AsyncSession, user_id: uuid.UUID, cursor: str | None, limit: int, type_filter: str | None,
) -> tuple[list[ReviewQueue], str | None, bool]:
    """List review queue items with cursor pagination."""
    raise NotImplementedError


async def get_review_item(db: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID) -> ReviewQueue | None:
    """Get a review item with associated content."""
    raise NotImplementedError


async def approve_item(db: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID, edited_content: str | None) -> ReviewQueue:
    """Approve a review item, optionally with edited content."""
    raise NotImplementedError


async def reject_item(db: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID, reason: str) -> ReviewQueue:
    """Reject a review item with a reason."""
    raise NotImplementedError


async def regenerate_item(db: AsyncSession, user_id: uuid.UUID, item_id: uuid.UUID, instructions: str) -> str:
    """Regenerate content for a review item. Returns task_id."""
    raise NotImplementedError


async def bulk_approve(db: AsyncSession, user_id: uuid.UUID, item_ids: list[uuid.UUID]) -> int:
    """Approve multiple items at once. Returns count of approved items."""
    raise NotImplementedError
