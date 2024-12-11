from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.utils.authPerm import permiso_requerido
from src.controllers.rolPermisoController import (
    create_rol_permiso,
    get_all_rol_permisos,
    get_rol_permiso_by_id,
    delete_rol_permiso,
)
from src.schemas.rolPermisoSchema import RolPermisoCreate, RolPermisoResponse
from uuid import UUID

ROL_PERMISO_ROUTER = APIRouter()

@ROL_PERMISO_ROUTER.post("/rol-permisos/", response_model=RolPermisoResponse)
async def create_rol_permiso_route(rol_permiso_data: RolPermisoCreate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await create_rol_permiso(db, rol_permiso_data)

@ROL_PERMISO_ROUTER.get("/rol-permisos/", response_model=list[RolPermisoResponse])
async def get_all_rol_permisos_route(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await get_all_rol_permisos(db)

@ROL_PERMISO_ROUTER.get("/rol-permisos/{rol_permiso_id}", response_model=RolPermisoResponse)
async def get_rol_permiso_by_id_route(rol_permiso_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await get_rol_permiso_by_id(db, rol_permiso_id)

@ROL_PERMISO_ROUTER.delete("/rol-permisos/{rol_permiso_id}")
async def delete_rol_permiso_route(rol_permiso_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await delete_rol_permiso(db, rol_permiso_id)
