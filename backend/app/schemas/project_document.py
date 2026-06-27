# app/schemas/project_document.py

from datetime import datetime
from pydantic import BaseModel


class ProjectDocumentBase(BaseModel):
    tenant_id: int | None = None
    project_id: int
    uploaded_by: int
    file_name: str
    file_path: str
    file_size: int | None = None
    mime_type: str | None = None
    document_type: str = "OTHER"


class ProjectDocumentCreate(ProjectDocumentBase):
    pass


class ProjectDocumentOut(ProjectDocumentBase):
    id: int
    uploaded_at: datetime

    model_config = {
        "from_attributes": True
    }
