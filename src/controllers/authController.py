from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.usuarioModel import Usuario
from src.utils.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BLACKLIST = set()

async def login(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(Usuario).filter(Usuario.nombre_usuario == username))
    user = result.scalar()

    if not user or not pwd_context.verify(password, user.contrasena_cifrada):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # Generar token JWT
    expiration = datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    token = jwt.encode({"sub": user.nombre_usuario, "exp": expiration}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Guardar el token en la base de datos
    user.jsonwebtoken = token
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"access_token": token, "token_type": "bearer"}


async def logout(db: AsyncSession, token: str, username: str):
    try:
        # Buscar al usuario por el nombre de usuario
        result = await db.execute(select(Usuario).filter(Usuario.nombre_usuario == username))
        user = result.scalar()
        if user and user.jsonwebtoken == token:
            user.jsonwebtoken = None  # Eliminar el token de la base de datos
            db.add(user)
            await db.commit()
            return {"message": "Sesión cerrada correctamente"}
        raise HTTPException(status_code=401, detail="Token inválido o ya expirado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cerrar sesión: {str(e)}")