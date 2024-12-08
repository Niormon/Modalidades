from pydantic import BaseModel
from datetime import date
from typing import Optional

# Esquema para la creación de un estudiante
class StudentCreate(BaseModel):
    codigo: str
    nombre: str
    cedula: str
    correo: str
    numero_telefonico: str
    fecha_nacimiento: date
    estudiante_graduado: bool = False

    class Config:
        orm_mode = True

# Esquema para la respuesta de un estudiante
class StudentResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    cedula: str
    correo: str
    numero_telefonico: str
    fecha_nacimiento: date
    estudiante_graduado: bool

    class Config:
        orm_mode = True

# Esquema para la actualización de un estudiante
class StudentUpdate(BaseModel):
    codigo: Optional[str]
    nombre: Optional[str]
    cedula: Optional[str]
    correo: Optional[str]
    numero_telefonico: Optional[str]
    fecha_nacimiento: Optional[date]
    estudiante_graduado: Optional[bool]

    class Config:
        from_attributes = True  # O 'orm_mode' dependiendo de la versión de Pydantic