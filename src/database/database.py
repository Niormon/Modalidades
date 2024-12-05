import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno desde el archivo .env
# Especificar la ruta al archivo .env en la raíz del proyecto
dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'  # Subir tres niveles para llegar a la raíz
load_dotenv(dotenv_path=dotenv_path)

# Obtener la URL de la base de datos del archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")  # Verifica que se carga correctamente

# Crear el motor de la base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión asíncrona
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Función para obtener la sesión
async def get_db():
    async with SessionLocal() as session:
        yield session

print("DATABASE_URL:", os.getenv("DATABASE_URL"))