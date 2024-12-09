from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from src.database.database import Base

class TrackingMode(Base):
    __tablename__ = "modalidad_seguimiento"

    id = Column(Integer, primary_key=True, index=True)
    modalidad_id = Column(Integer, ForeignKey("modalidad.id", ondelete="CASCADE"))
    estudiante_id = Column(Integer, ForeignKey("estudiante.id", ondelete="CASCADE"))
    profesor_id = Column(Integer, ForeignKey("profesor.id", ondelete="CASCADE"))
    institucion_id = Column(Integer, ForeignKey("institucion.id", ondelete="CASCADE"))
    modalidad_grado_activa = Column(Boolean, nullable=False, default=True)
    descripcion = Column(Text, nullable=True)
    nombre_jurado_1 = Column(String(100), nullable=True)
    nombre_jurado_2 = Column(String(100), nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones con importaciones diferidas
    modality = relationship("Modality", back_populates="tracking_modes")
    institution = relationship("Institution", back_populates="tracking_modes")
    student = relationship("Estudiante", back_populates="tracking_modes", lazy="joined")
    teacher = relationship("Teacher", back_populates="tracking_modes")
