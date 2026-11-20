from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.processing_job import ProcessingJob
from app.models.file import File as FileModel
from app.models.user import User
from app.schemas.processing_job import ProcessingJobResponse
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/processing-jobs",
    tags=["Processing Jobs"]
)


@router.get("/", response_model=list[ProcessingJobResponse])
def get_processing_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(ProcessingJob).join(
        FileModel,
        ProcessingJob.file_id == FileModel.id
    ).filter(
        FileModel.user_id == current_user.id
    ).all()

    return jobs


@router.get("/{job_id}", response_model=ProcessingJobResponse)
def get_processing_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(ProcessingJob).join(
        FileModel,
        ProcessingJob.file_id == FileModel.id
    ).filter(
        ProcessingJob.id == job_id,
        FileModel.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Processing job not found"
        )

    return job


@router.get("/{job_id}/result")
def get_processing_result(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(ProcessingJob).join(
        FileModel,
        ProcessingJob.file_id == FileModel.id
    ).filter(
        ProcessingJob.id == job_id,
        FileModel.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Processing job not found"
        )

    if job.status != "SUCCESS":
        raise HTTPException(
            status_code=409,
            detail=f"Processing is not complete. Current status: {job.status}"
        )

    return job.result