import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, Text, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from src.database.database import Base

class TrackingMode(Base):
    __tablename__ = "modalidad_seguimiento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    modalidad_id = Column(UUID(as_uuid=True), ForeignKey("modalidad.id", ondelete="CASCADE"))
    estudiante_id = Column(UUID(as_uuid=True), ForeignKey("estudiante.id", ondelete="CASCADE"))
    profesor_id = Column(UUID(as_uuid=True), ForeignKey("profesor.id", ondelete="CASCADE"))
    institucion_id = Column(UUID(as_uuid=True), ForeignKey("institucion.id", ondelete="CASCADE"))
    modalidad_grado_activa = Column(Boolean, nullable=False, default=True)
    descripcion = Column(Text, nullable=True)
    nombre_jurado_1 = Column(String(100), nullable=True)
    nombre_jurado_2 = Column(String(100), nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones con importaciones diferidas
    modality = relationship("Modality", back_populates="tracking_modes")
    institution = relationship("Institution", back_populates="tracking_modes")
    student = relationship("Student", back_populates="tracking_modes", lazy="joined")
    teacher = relationship("Teacher", back_populates="tracking_modes")
