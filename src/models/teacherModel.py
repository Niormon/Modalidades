from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Teacher(Base):
    __tablename__ = "profesor"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    numero_telefonico = Column(String(15), nullable=True)


    # Relación inversa con TrackingMode
    tracking_modes = relationship(
        "TrackingMode",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )