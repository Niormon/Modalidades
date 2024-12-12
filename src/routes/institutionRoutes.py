from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.utils.authPerm import permiso_requerido
from src.schemas.institutionSchema import InstitutionCreate, InstitutionUpdate, InstitutionResponse
from uuid import UUID
from src.controllers.institutionController import (
    get_institutions, get_institution, create_institution, update_institution, delete_institution
)

INSTITUTION_ROUTES = APIRouter()

@INSTITUTION_ROUTES.get("/institutions/", response_model=list[InstitutionResponse])
async def list_institutions(db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Consultar"))
):
    return await get_institutions(db)

@INSTITUTION_ROUTES.get("/institutions/{institution_id}", response_model=InstitutionResponse)
async def get_institution_by_id(institution_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Consultar"))
):
    institution = await get_institution(db, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return institution

@INSTITUTION_ROUTES.post("/institutions/", response_model=InstitutionResponse)
async def create_institution_endpoint(institution: InstitutionCreate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Operar"))
):
    return await create_institution(db, institution)

@INSTITUTION_ROUTES.put("/institutions/{institution_id}", response_model=InstitutionResponse)
async def update_institution_endpoint(institution_id: UUID, institution: InstitutionUpdate, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Operar"))
):
    db_institution = await update_institution(db, institution_id, institution)
    if not db_institution:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return db_institution

@INSTITUTION_ROUTES.delete("/institutions/{institution_id}", response_model=dict)
async def delete_institution_endpoint(institution_id: UUID, db: AsyncSession = Depends(get_db),
    _: None = Depends(permiso_requerido("Operar"))
):
    db_institution = await delete_institution(db, institution_id)
    if not db_institution:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return db_institution
