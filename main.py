from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.database import get_db
from src.models.studentModel import Estudiante  

app = FastAPI()

# Ruta de ejemplo que interactúa con la base de datos
@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    # Este ejemplo asume que tienes alguna tabla de "Estudiantes"
    result = await db.execute(select(Estudiante))  # Ejemplo de consulta
    estudiantes = result.scalars().all()  # Devuelve los resultados de la consulta
    return estudiantes

@app.get("/")
async def root():
    return {"message": "Hello World"}