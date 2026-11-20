from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.sql import func

from app.database import Base


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(String, unique=True, nullable=False)

    file_id = Column(Integer, ForeignKey("file.id"), nullable=False)

    status = Column(String, default="PENDING", nullable=False)

    result = Column(JSON, nullable=True)

    error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    completed_at = Column(DateTime(timezone=True), nullable=True)
