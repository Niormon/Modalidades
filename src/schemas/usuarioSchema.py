from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from src.schemas.rolSchema import RolResponse

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    contrasena: str
    id_rol: Optional[UUID]

class UsuarioResponse(BaseModel):
    id: UUID
    nombre_usuario: str
    id_rol: Optional[UUID]
    rol: Optional[RolResponse]  # Incluye información del rol

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    id_rol: Optional[UUID] = None

    class Config:
        from_attributes = True
