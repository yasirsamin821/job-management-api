from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    description: str | None = None


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str | None
    user_id: int

    model_config = ConfigDict(from_attributes=True)

