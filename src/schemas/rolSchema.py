from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: Optional[str]

class RolUpdate(BaseModel):
    nombre_rol: Optional[str]
    descripcion: Optional[str]

class RolResponse(BaseModel):
    id: UUID
    nombre_rol: str
    descripcion: Optional[str]

    class Config:
        from_attributes = True
