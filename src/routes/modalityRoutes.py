from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.utils.authPerm import permiso_requerido
from src.schemas.modalitySchema import ModalityCreate, ModalityUpdate, ModalityResponse
from uuid import UUID
from src.controllers.modalityController import (
    get_modalities, get_modality, create_modality, update_modality, delete_modality
)

MODALITY_ROUTES = APIRouter()

@MODALITY_ROUTES.get("/modalities/", response_model=list[ModalityResponse])
async def list_modalities(db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Consultar"))
):
    return await get_modalities(db)

@MODALITY_ROUTES.get("/modalities/{modality_id}", response_model=ModalityResponse)
async def get_modality_by_id(modality_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Consultar"))
):
    return await get_modality(db, modality_id)

@MODALITY_ROUTES.post("/modalities/", response_model=ModalityResponse)
async def create_modality_endpoint(modality: ModalityCreate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await create_modality(db, modality)

@MODALITY_ROUTES.put("/modalities/{modality_id}", response_model=ModalityResponse)
async def update_modality_endpoint(modality_id: UUID, modality: ModalityUpdate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await update_modality(db, modality_id, modality)

@MODALITY_ROUTES.delete("/modalities/{modality_id}", response_model=dict)
async def delete_modality_endpoint(modality_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Admin"))
):
    return await delete_modality(db, modality_id)