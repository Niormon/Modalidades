from pydantic import BaseModel
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
