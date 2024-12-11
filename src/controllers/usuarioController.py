from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi import HTTPException
from passlib.context import CryptContext
from src.models.usuarioModel import Usuario
from src.schemas.usuarioSchema import UsuarioCreate, UsuarioUpdate
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

# Actualisar usuario

async def update_usuario(db: AsyncSession, usuario_id: str, usuario_data: UsuarioUpdate):
    try:
        # Buscar el usuario por ID
        result = await db.execute(select(Usuario).filter(Usuario.id == usuario_id))
        usuario = result.scalar()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Validar que el nuevo nombre de usuario no esté en uso por otro usuario
        if usuario_data.nombre_usuario and usuario_data.nombre_usuario != usuario.nombre_usuario:
            existing_user = await db.execute(
                select(Usuario).filter(Usuario.nombre_usuario == usuario_data.nombre_usuario)
            )
            if existing_user.scalar():
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

        # Actualizar campos si están presentes en los datos de entrada
        if usuario_data.nombre_usuario:
            usuario.nombre_usuario = usuario_data.nombre_usuario

        if usuario_data.contrasena:
            usuario.contrasena_cifrada = pwd_context.hash(usuario_data.contrasena)

        if usuario_data.id_rol:
            usuario.id_rol = usuario_data.id_rol

        await db.commit()
        await db.refresh(usuario)
        return usuario
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar el usuario: {str(e)}")

# Eliminar usuario
async def delete_user(db: AsyncSession, user_id: UUID):
    user = await get_user_by_id(db, user_id)
    await db.execute(delete(Usuario).where(Usuario.id == user_id))
    await db.commit()
    return {"message": "Usuario eliminado exitosamente"}
