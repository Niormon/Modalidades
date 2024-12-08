from pydantic import BaseModel, EmailStr
from typing import Optional

class TeacherBase(BaseModel):
    cedula: str
    nombre: str
    correo: EmailStr
    numero_telefonico: Optional[str] = None

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: int

    class Config:
        from_attributes = True
