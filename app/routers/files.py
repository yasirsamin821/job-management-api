from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
import uuid
from pathlib import Path
import shutil

from app.database import get_db
from app.models import processing_job
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileResponse
from app.auth.dependencies import get_current_user
from app.tasks.csv_tasks import process_csv
from app.models.processing_job import ProcessingJob

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {".csv"}
ALLOWED_CONTENT_TYPES = {"text/csv"}

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type"
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 5 MB limit"
        )

    unique_filename = f"{uuid.uuid4()}.csv"

    file_path = UPLOAD_DIR / unique_filename

    await file.seek(0)

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_file = FileModel(
        filename=file.filename,
        file_path=str(file_path),
        file_size=len(contents),
        user_id=current_user.id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    task_id = str(uuid.uuid4())

    processing_job = ProcessingJob(
        task_id=task_id,
        file_id=db_file.id,
        status='PENDING'
    )
    db.add(processing_job)
    db.commit()
    db.refresh(processing_job)

    process_csv.apply_async(
        args=[str(file_path)],
        task_id=task_id,
    )

    return {
        "id__": db_file.id,
        "filename": db_file.filename,
        "file_path": db_file.file_path,
        "file_size": db_file.file_size,
        "user_id": db_file.user_id,
        "message": "File uploaded and preprocessing started",
        'task_id': task_id,
        'preprocessing_job_id': processing_job.id
    }


@router.get("/", response_model=list[FileResponse])
def get_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    files = db.query(FileModel).filter(
        FileModel.user_id == current_user.id
    ).all()

    return files


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    ).first()

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return file