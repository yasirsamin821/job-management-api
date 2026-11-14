from pydantic import BaseModel

class FileResponse(BaseModel):

    id: int
    filename: str
    file_path: str
    file_size: int
    user_id: int

    model_config = {'from_attributes': True}