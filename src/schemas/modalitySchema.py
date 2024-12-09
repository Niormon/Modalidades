from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class ModalityBase(BaseModel):
    modality: str
    description: Optional[str] = None

class ModalityCreate(ModalityBase):
    pass

class ModalityUpdate(ModalityBase):
    pass

class ModalityResponse(BaseModel):
    id: UUID
    modality: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # Para que Pydantic entienda cómo mapear desde SQLAlchemy
