from sqlalchemy import Column, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.database import Base

class RolPermiso(Base):
    __tablename__ = "rol_permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    id_rol = Column(UUID(as_uuid=True), ForeignKey("rol.id", ondelete="CASCADE"), nullable=False)
    id_permiso = Column(UUID(as_uuid=True), ForeignKey("permiso.id", ondelete="CASCADE"), nullable=False)

    # Relaciones
    rol = relationship("Rol", back_populates="rol_permisos", lazy="joined")
    permiso = relationship("Permiso", lazy="joined")

    # Evitar duplicados
    __table_args__ = (UniqueConstraint("id_rol", "id_permiso", name="uq_rol_permiso"),)
