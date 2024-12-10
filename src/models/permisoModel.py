from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.database import Base
import uuid

class Permiso(Base):
    __tablename__ = "permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    nombre_permiso = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
