"""Review Queue API endpoints — API Contract Section 4.6.

6 endpoints: list, get, approve, reject, regenerate, bulk-approve.
"""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse, TaskResponse
from app.schemas.review import (
    ApproveRequest,
    BulkApproveRequest,
    BulkApproveResponse,
    RegenerateRequest,
    RejectRequest,
    ReviewQueueItem,
    ReviewQueueItemDetail,
)

router = APIRouter(prefix="/review")


@router.get("", response_model=PaginatedResponse[ReviewQueueItem])
async def list_review_items(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    type_filter: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ReviewQueueItem]:
    """List review queue items with cursor pagination."""
    raise NotImplementedError


@router.get("/{item_id}", response_model=DataResponse[ReviewQueueItemDetail])
async def get_review_item(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ReviewQueueItemDetail]:
    """Get a review queue item with full detail."""
    raise NotImplementedError


@router.post("/{item_id}/approve", response_model=DataResponse[ReviewQueueItem])
async def approve_item(
    item_id: uuid.UUID,
    body: ApproveRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ReviewQueueItem]:
    """Approve a review queue item, optionally with edited content."""
    raise NotImplementedError


@router.post("/{item_id}/reject", response_model=DataResponse[ReviewQueueItem])
async def reject_item(
    item_id: uuid.UUID,
    body: RejectRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[ReviewQueueItem]:
    """Reject a review queue item with a reason."""
    raise NotImplementedError


@router.post("/{item_id}/regenerate", response_model=TaskResponse)
async def regenerate_item(
    item_id: uuid.UUID,
    body: RegenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Regenerate content for a review queue item."""
    raise NotImplementedError


@router.post("/bulk-approve", response_model=BulkApproveResponse)
async def bulk_approve(
    body: BulkApproveRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BulkApproveResponse:
    """Approve multiple review queue items at once."""
    raise NotImplementedError
