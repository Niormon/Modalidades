from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class Modality(Base):
    __tablename__ = "modalidad"

    id = Column(Integer, primary_key=True, index=True)
    modalidad = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relación inversa con TrackingMode
    tracking_modes = relationship(
        "TrackingMode",
        back_populates="modality",
        cascade="all, delete-orphan"
    )
