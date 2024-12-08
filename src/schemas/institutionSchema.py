from pydantic import BaseModel, EmailStr
from typing import Optional

class InstitutionBase(BaseModel):
    nombre: str
    pais_ciudad: Optional[str] = None
    direccion: Optional[str] = None
    numero_telefonico: Optional[str] = None
    correo: Optional[EmailStr] = None

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionUpdate(InstitutionBase):
    pass

class InstitutionResponse(InstitutionBase):
    id: int

    class Config:
        orm_mode = True
