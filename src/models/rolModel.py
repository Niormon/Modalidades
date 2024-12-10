import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from src.database.database import Base

class Rol(Base):
    __tablename__ = "rol"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    # llaves foraneas
    usuarios = relationship("Usuario", back_populates="rol", lazy="dynamic")
    rol_permisos = relationship("RolPermiso", back_populates="rol", cascade="all, delete-orphan")