from pydantic import BaseModel
from uuid import UUID

class PermisoCreate(BaseModel):
    nombre_permiso: str
    descripcion: str

class PermisoResponse(BaseModel):
    id: UUID
    nombre_permiso: str
    descripcion: str

    class Config:
        from_attributes = True
