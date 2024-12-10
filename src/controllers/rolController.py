from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi import HTTPException
from src.models.rolModel import Rol
from src.schemas.rolSchema import RolCreate, RolUpdate
from uuid import UUID

# Crear un rol
async def create_rol(db: AsyncSession, rol: RolCreate):
    try:
        new_rol = Rol(nombre_rol=rol.nombre_rol, descripcion=rol.descripcion)
        db.add(new_rol)
        await db.commit()
        return new_rol
    except IntegrityError as e:
        await db.rollback()
        if "nombre_rol" in str(e.orig):
            raise HTTPException(status_code=400, detail="El nombre del rol ya existe")
        raise HTTPException(status_code=500, detail="Error creando rol")

# Obtener todos los roles
async def get_roles(db: AsyncSession):
    try:
        result = await db.execute(select(Rol))
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener roles: {str(e)}")

# Obtener rol por ID
async def get_rol_by_id(db: AsyncSession, rol_id: UUID):
    try:
        result = await db.execute(select(Rol).filter(Rol.id == rol_id))
        rol = result.scalar()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener rol: {str(e)}")

# Actualizar un rol
async def update_rol(db: AsyncSession, rol_id: UUID, rol: RolUpdate):
    try:
        existing_rol = await get_rol_by_id(db, rol_id)
        for key, value in rol.dict(exclude_unset=True).items():
            setattr(existing_rol, key, value)
        await db.commit()
        return existing_rol
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando rol: {str(e)}")

# Eliminar un rol
async def delete_rol(db: AsyncSession, rol_id: UUID):
    try:
        existing_rol = await get_rol_by_id(db, rol_id)
        await db.execute(delete(Rol).where(Rol.id == rol_id))
        await db.commit()
        return {"message": "Rol eliminado exitosamente"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error eliminando rol: {str(e)}")
