import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class Institution(Base):
    __tablename__ = "institucion"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    pais_ciudad = Column(String(100))
    direccion = Column(Text)
    numero_telefonico = Column(String(15))
    correo = Column(String(100))

    # Relación inversa con TrackingMode
    tracking_modes = relationship(
        "TrackingMode",
        back_populates="institution",
        cascade="all, delete-orphan"
    )