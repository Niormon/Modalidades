import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class Modality(Base):
    __tablename__ = "modalidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    modalidad = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relación inversa con TrackingMode
    tracking_modes = relationship(
        "TrackingMode",
        back_populates="modality",
        cascade="all, delete-orphan"
    )
