from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.permisoModel import Permiso

async def create_permiso(db: AsyncSession, permiso_data):
    try:
        new_permiso = Permiso(**permiso_data.dict())
        db.add(new_permiso)
        await db.commit()
        await db.refresh(new_permiso)
        return new_permiso
    except IntegrityError as e:
        # Detectar violación de unicidad
        if "permiso_nombre_permiso_key" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="El nombre del permiso ya existe. Por favor, elige otro."
            )
        raise HTTPException(status_code=400, detail=f"Error al crear permiso: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

async def get_all_permisos(db: AsyncSession):
    result = await db.execute(select(Permiso))
    return result.scalars().all()

async def get_permiso_by_id(db: AsyncSession, permiso_id):
    result = await db.execute(select(Permiso).filter(Permiso.id == permiso_id))
    permiso = result.scalar()
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso

async def update_permiso(db: AsyncSession, permiso_id, permiso_data):
    permiso = await get_permiso_by_id(db, permiso_id)
    for key, value in permiso_data.dict(exclude_unset=True).items():
        setattr(permiso, key, value)
    db.add(permiso)
    await db.commit()
    await db.refresh(permiso)
    return permiso

async def delete_permiso(db: AsyncSession, permiso_id):
    permiso = await get_permiso_by_id(db, permiso_id)
    await db.delete(permiso)
    await db.commit()
    return {"message": "Permiso eliminado correctamente"}
