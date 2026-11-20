from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any


class ProcessingJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: str
    file_id: int
    status: str
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None