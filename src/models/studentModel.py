from sqlalchemy import Column, Integer, String, Boolean, Date
from src.database.database import Base

class Estudiante(Base):
    __tablename__ = 'estudiante'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    correo = Column(String(100), nullable=False)
    numero_telefonico = Column(String(15))
    fecha_nacimiento = Column(Date)
    estudiante_graduado = Column(Boolean, default=False)
