from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class TrackingModeBase(BaseModel):
    modalidad_id: int
    estudiante_id: int
    profesor_id: int
    institucion_id: int
    modalidad_grado_activa: Optional[bool] = True
    descripcion: Optional[str] = None
    nombre_jurado_1: str
    nombre_jurado_2: str
    fecha_inicio: date
    fecha_fin: date

class TrackingModeCreate(TrackingModeBase):
    pass

class TrackingModeUpdate(TrackingModeBase):
    pass

class TrackingModeResponse(TrackingModeBase):
    id: int

    class Config:
        from_attributes = True

class ModalityBase(BaseModel):
    id: int
    modalidad: str
    descripcion: Optional[str]

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    id: int
    codigo: str
    nombre: str
    cedula: str
    correo: str
    numero_telefonico: str
    fecha_nacimiento: date
    estudiante_graduado: bool
    
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    id: int
    cedula: str
    nombre: str
    correo: str
    numero_telefonico: str

    class Config:
        from_attributes = True

class InstitutionBase(BaseModel):
    id: int
    nombre: str
    pais_ciudad: str
    direccion: str
    numero_telefonico: str
    correo: str

    class Config:
        from_attributes = True

class TrackingModeResponseGet(BaseModel):
    id: int
    modalidad_grado_activa: bool
    descripcion: Optional[str]
    nombre_jurado_1: Optional[str]
    nombre_jurado_2: Optional[str]
    fecha_inicio: Optional[str]  # Vamos a convertir esta fecha
    fecha_fin: Optional[str]     # Vamos a convertir esta fecha
    
    modality: ModalityBase
    student: StudentBase
    teacher: TeacherBase
    institution: InstitutionBase

    # Usamos un validador para convertir las fechas
    @validator('fecha_inicio', 'fecha_fin', pre=True, always=True)
    def format_date(cls, v):
        if isinstance(v, date):
            return v.strftime('%Y-%m-%d')  # Convierte la fecha a formato string 'YYYY-MM-DD'
        return v

    class Config:
        from_attributes = True