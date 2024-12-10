from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.controllers.permisoController import (
    create_permiso,
    get_all_permisos,
    get_permiso_by_id,
    update_permiso,
    delete_permiso,
)
from src.schemas.permisoSchema import PermisoCreate, PermisoResponse
from uuid import UUID

PERMISO_ROUTER = APIRouter()

@PERMISO_ROUTER.post("/permisos/", response_model=PermisoResponse)
async def create_permission_route(permiso_data: PermisoCreate, db: AsyncSession = Depends(get_db)):
    return await create_permiso(db, permiso_data)

@PERMISO_ROUTER.get("/permisos/", response_model=list[PermisoResponse])
async def get_all_permissions_route(db: AsyncSession = Depends(get_db)):
    return await get_all_permisos(db)

@PERMISO_ROUTER.get("/permisos/{permiso_id}", response_model=PermisoResponse)
async def get_permission_by_id_route(permiso_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_permiso_by_id(db, permiso_id)

@PERMISO_ROUTER.put("/permisos/{permiso_id}", response_model=PermisoResponse)
async def update_permission_route(permiso_id: UUID, permiso_data: PermisoCreate, db: AsyncSession = Depends(get_db)):
    return await update_permiso(db, permiso_id, permiso_data)

@PERMISO_ROUTER.delete("/permisos/{permiso_id}")
async def delete_permission_route(permiso_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_permiso(db, permiso_id)
