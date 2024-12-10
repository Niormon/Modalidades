from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi import HTTPException
from passlib.context import CryptContext
from src.models.usuarioModel import Usuario
from src.schemas.usuarioSchema import UsuarioCreate
from uuid import UUID

# Configuración de cifrado
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear un usuario
async def create_user(db: AsyncSession, user: UsuarioCreate):
    try:
        hashed_password = pwd_context.hash(user.contrasena)
        new_user = Usuario(
            nombre_usuario=user.nombre_usuario,
            contrasena_cifrada=hashed_password,
            id_rol=user.id_rol,
        )
        db.add(new_user)
        await db.commit()

        # Refresca el objeto para cargar relaciones
        await db.refresh(new_user)

        # Carga explícita de la relación `rol`
        result = await db.execute(
            select(Usuario).options(joinedload(Usuario.rol)).filter(Usuario.id == new_user.id)
        )
        user_with_role = result.scalar()

        return user_with_role
    except IntegrityError as e:
        await db.rollback()
        if "nombre_usuario" in str(e.orig):
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        raise HTTPException(status_code=500, detail="Error creando usuario")

# Obtener todos los usuarios
async def get_users(db: AsyncSession):
    try:
        result = await db.execute(
            select(Usuario).options(joinedload(Usuario.rol))  # Carga la información del rol
        )
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

# Obtener usuario por ID
async def get_user_by_id(db: AsyncSession, user_id: UUID):
    try:
        result = await db.execute(
            select(Usuario)
            .options(joinedload(Usuario.rol))  # Carga la información del rol
            .filter(Usuario.id == user_id)
        )
        user = result.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

# Eliminar usuario
async def delete_user(db: AsyncSession, user_id: UUID):
    user = await get_user_by_id(db, user_id)
    await db.execute(delete(Usuario).where(Usuario.id == user_id))
    await db.commit()
    return {"message": "Usuario eliminado exitosamente"}
