import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contrasena_cifrada = Column(Text, nullable=False)
    id_rol = Column(UUID(as_uuid=True), ForeignKey("rol.id", ondelete="CASCADE"))
    jsonwebtoken = Column(Text, nullable=True)

    # Relación con Rol
    rol = relationship("Rol", back_populates="usuarios")
