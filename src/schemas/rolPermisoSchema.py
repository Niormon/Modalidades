from pydantic import BaseModel
from uuid import UUID
from src.schemas.rolSchema import RolResponse
from src.schemas.permisoSchema import PermisoResponse

class RolPermisoCreate(BaseModel):
    id_rol: UUID
    id_permiso: UUID

class RolPermisoResponse(BaseModel):
    id: UUID
    rol: RolResponse
    permiso: PermisoResponse

    class Config:
        from_attributes = True
