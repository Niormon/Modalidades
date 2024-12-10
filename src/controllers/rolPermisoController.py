from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import HTTPException
from src.models.rolPermisoModel import RolPermiso
from src.models.rolModel import Rol
from src.models.permisoModel import Permiso

async def create_rol_permiso(db: AsyncSession, rol_permiso_data):
    try:
        # Verificar que el rol y el permiso existan
        rol = await db.execute(select(Rol).filter(Rol.id == rol_permiso_data.id_rol))
        if not rol.scalar():
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        permiso = await db.execute(select(Permiso).filter(Permiso.id == rol_permiso_data.id_permiso))
        if not permiso.scalar():
            raise HTTPException(status_code=404, detail="Permiso no encontrado")

        # Verificar si la relación ya existe
        existing_relation = await db.execute(
            select(RolPermiso)
            .filter(
                RolPermiso.id_rol == rol_permiso_data.id_rol,
                RolPermiso.id_permiso == rol_permiso_data.id_permiso
            )
        )
        if existing_relation.scalar():
            raise HTTPException(
                status_code=400, 
                detail="La relación entre este rol y permiso ya existe."
            )

        # Crear la relación rol-permiso
        new_rol_permiso = RolPermiso(**rol_permiso_data.dict())
        db.add(new_rol_permiso)
        await db.commit()
        await db.refresh(new_rol_permiso)
        return new_rol_permiso
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al crear la relación: Violación de restricción única."
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al crear la relación: {str(e)}"
        )

async def get_all_rol_permisos(db: AsyncSession):
    result = await db.execute(select(RolPermiso).join(Rol).join(Permiso))
    return result.scalars().all()

async def get_rol_permiso_by_id(db: AsyncSession, rol_permiso_id):
    result = await db.execute(
        select(RolPermiso).filter(RolPermiso.id == rol_permiso_id).join(Rol).join(Permiso)
    )
    rol_permiso = result.scalar()
    if not rol_permiso:
        raise HTTPException(status_code=404, detail="Rol-Permiso no encontrado")
    return rol_permiso

async def delete_rol_permiso(db: AsyncSession, rol_permiso_id):
    rol_permiso = await get_rol_permiso_by_id(db, rol_permiso_id)
    await db.delete(rol_permiso)
    await db.commit()
    return {"message": "Relación Rol-Permiso eliminada correctamente"}
