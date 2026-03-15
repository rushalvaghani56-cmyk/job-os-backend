"""Content generation tasks — async resume, cover letter, answer generation."""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="content.generate_resume")
def generate_resume(self, user_id: str, job_id: str, profile_id: str, instructions: str | None = None) -> dict:
    """Generate a tailored resume using AI.

    Steps:
    1. Load job, profile, skills, work experience
    2. Call AI provider with structured prompt
    3. Store generated document in R2
    4. Create Document record with quality_score
    5. Create ReviewQueue item for human review
    """
    raise NotImplementedError


@celery_app.task(bind=True, name="content.generate_cover_letter")
def generate_cover_letter(self, user_id: str, job_id: str, profile_id: str) -> dict:
    """Generate a cover letter using AI."""
    raise NotImplementedError


@celery_app.task(bind=True, name="content.generate_answers")
def generate_answers(self, user_id: str, job_id: str, questions: list[str]) -> dict:
    """Generate answers to application questions using AI."""
    raise NotImplementedError


@celery_app.task(bind=True, name="content.regenerate_document")
def regenerate_document(self, user_id: str, document_id: str, instructions: str) -> dict:
    """Regenerate a document with new instructions."""
    raise NotImplementedError
