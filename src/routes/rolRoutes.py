from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers.rolController import (
    create_rol,
    get_roles,
    get_rol_by_id,
    update_rol,
    delete_rol,
)
from src.schemas.rolSchema import RolCreate, RolUpdate, RolResponse
from src.utils.authPerm import permiso_requerido
from src.database.database import get_db
from uuid import UUID

ROL_ROUTER = APIRouter()

@ROL_ROUTER.post("/roles/", response_model=RolResponse)
async def create_new_rol(rol: RolCreate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await create_rol(db, rol)

@ROL_ROUTER.get("/roles/", response_model=list[RolResponse])
async def read_roles(db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await get_roles(db)

@ROL_ROUTER.get("/roles/{rol_id}", response_model=RolResponse)
async def read_rol(rol_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await get_rol_by_id(db, rol_id)

@ROL_ROUTER.put("/roles/{rol_id}", response_model=RolResponse)
async def update_existing_rol(rol_id: UUID, rol: RolUpdate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await update_rol(db, rol_id, rol)

@ROL_ROUTER.delete("/roles/{rol_id}")
async def remove_rol(rol_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await delete_rol(db, rol_id)
