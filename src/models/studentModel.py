import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.orm import relationship
from src.database.database import Base

class Student(Base):
    __tablename__ = 'estudiante'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    correo = Column(String(100), nullable=False)
    numero_telefonico = Column(String(15))
    fecha_nacimiento = Column(Date)
    estudiante_graduado  = Column(Boolean, default=False)

    # Relación inversa con TrackingMode
    tracking_modes = relationship(
        "TrackingMode", 
        back_populates="student", 
        cascade="all, delete-orphan"
        )
