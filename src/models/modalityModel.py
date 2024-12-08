from sqlalchemy import Column, Integer, String, Text
from src.database.database import Base

class Modality(Base):
    __tablename__ = "modalidad"

    id = Column(Integer, primary_key=True, index=True)
    modalidad = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
