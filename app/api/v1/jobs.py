"""Jobs API endpoints — API Contract Section 4.3.

11 endpoints: list, get, manual create, status update, bookmark, skip,
score, generate, bulk-score, search, discover.
"""

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import DataResponse, PaginatedResponse, TaskResponse
from app.schemas.job import (
    BulkScoreRequest,
    DiscoverRequest,
    JobCreate,
    JobResponse,
    JobStatusUpdate,
)

router = APIRouter(prefix="/jobs")


@router.get("", response_model=PaginatedResponse[JobResponse])
async def list_jobs(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    sort: str | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    min_score: float | None = None,
    company: str | None = None,
    profile_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[JobResponse]:
    """List jobs with cursor pagination and filters."""
    raise NotImplementedError


@router.get("/search", response_model=DataResponse[list[JobResponse]])
async def search_jobs(
    q: str = Query(...),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[list[JobResponse]]:
    """Full-text search across jobs."""
    raise NotImplementedError


@router.get("/{job_id}", response_model=DataResponse[JobResponse])
async def get_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[JobResponse]:
    """Get a single job by ID."""
    raise NotImplementedError


@router.post("/manual", status_code=status.HTTP_201_CREATED, response_model=DataResponse[JobResponse])
async def create_job_manual(
    body: JobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[JobResponse]:
    """Manually add a job from URL or raw text."""
    raise NotImplementedError


@router.put("/{job_id}/status", response_model=DataResponse[JobResponse])
async def update_job_status(
    job_id: uuid.UUID,
    body: JobStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[JobResponse]:
    """Update a job's status."""
    raise NotImplementedError


@router.post("/{job_id}/bookmark", response_model=DataResponse[JobResponse])
async def bookmark_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[JobResponse]:
    """Bookmark a job."""
    raise NotImplementedError


@router.post("/{job_id}/skip", response_model=DataResponse[JobResponse])
async def skip_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DataResponse[JobResponse]:
    """Skip a job."""
    raise NotImplementedError


@router.post("/{job_id}/score", response_model=TaskResponse)
async def score_job(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Trigger async scoring for a single job."""
    raise NotImplementedError


@router.post("/{job_id}/generate", response_model=TaskResponse)
async def generate_content_for_job(
    job_id: uuid.UUID,
    instructions: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Trigger async content generation for a job."""
    raise NotImplementedError


@router.post("/bulk-score", response_model=TaskResponse)
async def bulk_score_jobs(
    body: BulkScoreRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Trigger bulk async scoring for multiple jobs."""
    raise NotImplementedError


@router.post("/discover", response_model=TaskResponse)
async def discover_jobs(
    body: DiscoverRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Trigger async job discovery for a profile."""
    raise NotImplementedError
