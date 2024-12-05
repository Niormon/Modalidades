from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Estudiante(Base):
    __tablename__ = 'estudiante'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nombre = Column(String)
    cedula = Column(String, unique=True)
    correo = Column(String)
    numero_telefonico = Column(String)
    fecha_nacimiento = Column(Date)
    estudiante_graduado = Column(Boolean, default=False)
