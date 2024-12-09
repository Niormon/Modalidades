from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.models.modalityModel import Modality
from src.schemas.modalitySchema import ModalityCreate, ModalityUpdate, ModalityResponse
from uuid import UUID

async def get_modalities(db: AsyncSession):
    result = await db.execute(select(Modality))
    modalities = result.scalars().all()
    # Mapear el resultado para que coincida con el esquema Pydantic
    return [
        ModalityResponse(
            id=modality.id,
            modality=modality.modalidad,
            description=modality.descripcion,
        )
        for modality in modalities
    ]

async def get_modality(db: AsyncSession, modality_id: UUID):
    modality = await db.get(Modality, modality_id)
    if not modality:
        raise HTTPException(status_code=404, detail="Modality not found")
    return ModalityResponse(
        id=modality.id,
        modality=modality.modalidad,
        description=modality.descripcion,
    )

async def create_modality(db: AsyncSession, modality: ModalityCreate):
    try:
        new_modality = Modality(
            modalidad=modality.modality,
            descripcion=modality.description,
        )
        db.add(new_modality)
        await db.commit()
        await db.refresh(new_modality)
        return ModalityResponse(
            id=new_modality.id,
            modality=new_modality.modalidad,
            description=new_modality.descripcion,
        )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Modality already exists")

async def update_modality(db: AsyncSession, modality_id: UUID, modality: ModalityUpdate):
    db_modality = await db.get(Modality, modality_id)
    if not db_modality:
        raise HTTPException(status_code=404, detail="Modality not found")

    # Validar si el nombre ya existe
    existing_modality = await db.execute(
        select(Modality).where(Modality.modalidad == modality.modality, Modality.id != modality_id)
    )
    if existing_modality.scalar():
        raise HTTPException(status_code=400, detail="A modality with this name already exists.")

    db_modality.modalidad = modality.modality
    db_modality.descripcion = modality.description
    await db.commit()
    await db.refresh(db_modality)

    return ModalityResponse(
        id=db_modality.id,
        modality=db_modality.modalidad,
        description=db_modality.descripcion,
    )

async def delete_modality(db: AsyncSession, modality_id: UUID):
    db_modality = await db.get(Modality, modality_id)
    if not db_modality:
        raise HTTPException(status_code=404, detail="Modality not found")

    await db.delete(db_modality)
    await db.commit()
    return {"message": "Modality deleted successfully"}
