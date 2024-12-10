from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers.usuarioController import (
    create_user,
    get_users,
    get_user_by_id,
    delete_user
)
from src.schemas.usuarioSchema import UsuarioCreate, UsuarioResponse
from src.database.database import get_db
from uuid import UUID

USUARIO_ROUTER = APIRouter()

@USUARIO_ROUTER.post("/usuarios/", response_model=UsuarioResponse)
async def create_new_user(user: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@USUARIO_ROUTER.get("/usuarios/", response_model=list[UsuarioResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@USUARIO_ROUTER.get("/usuarios/{user_id}", response_model=UsuarioResponse)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@USUARIO_ROUTER.delete("/usuarios/{user_id}")
async def remove_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_user(db, user_id)