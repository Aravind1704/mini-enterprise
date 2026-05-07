from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentOut(BaseModel):
    id: int
    file_name: str
    file_path: str
    version: int
    uploaded_by: int
    task_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True