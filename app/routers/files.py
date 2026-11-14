from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from sqlalchemy.orm import Session
import uuid
from pathlib import Path
import shutil

from app.database import get_db
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileResponse

MAX_FILE_SIZE = 5 * 1024 * 1024
router = APIRouter()

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {".csv"}
ALLOWED_CONTENT_TYPES = {"text/csv"}

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      user_id: int = Form(...),
                      db: Session = Depends(get_db)
                      ):

    extension = file.filename.split(".")[-1].lower()

    if f".{extension}" not in ALLOWED_EXTENSIONS:
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
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        shutil.copyfileobj(file.file, buffer)
        db_file = FileModel(
            filename = file.filename,
            file_path = str(file_path),
            file_size = len(contents),
            user_id = user_id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "file_path": db_file.file_path,
        "file_size": db_file.file_size,
        "user_id": db_file.user_id,
        "message": "File uploaded successfully"
    }



@router.get('/', response_model=list[FileResponse])
def get_files(db: Session = Depends(get_db)):
    files = db.query(FileModel).all()

    return files


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file