from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.institutionModel import Institution
from src.schemas.institutionSchema import InstitutionCreate, InstitutionUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from uuid import UUID

async def get_institutions(db: AsyncSession):
    result = await db.execute(select(Institution))
    return result.scalars().all()

async def get_institution(db: AsyncSession, institution_id: UUID):
    return await db.get(Institution, institution_id)

async def create_institution(db: AsyncSession, institution: InstitutionCreate):
    try:
        new_institution = Institution(**institution.dict())
        db.add(new_institution)
        await db.commit()
        await db.refresh(new_institution)
        return new_institution
    except IntegrityError:
        await db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(
            status_code=400,
            detail="Ya existe una institución con el mismo nombre."
        )

async def update_institution(db: AsyncSession, institution_id: UUID, institution: InstitutionUpdate):
    try:
        # Verificar si el nombre ya existe en otra institución
        existing_institution = await db.execute(
            select(Institution).where(
                Institution.nombre == institution.nombre,
                Institution.id != institution_id  # Asegurar que no sea la misma institución
            )
        )
        if existing_institution.scalar():
            raise HTTPException(
                status_code=400,
                detail="Ya existe una institución con el mismo nombre."
            )

        # Obtener la institución a actualizar
        db_institution = await db.get(Institution, institution_id)
        if not db_institution:
            raise HTTPException(status_code=404, detail="Institución no encontrada")

        # Actualizar los valores
        for key, value in institution.dict(exclude_unset=True).items():
            setattr(db_institution, key, value)

        await db.commit()
        await db.refresh(db_institution)
        return db_institution
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar la institución."
        )

async def delete_institution(db: AsyncSession, institution_id: UUID):
    db_institution = await get_institution(db, institution_id)
    if not db_institution:
        return None
    await db.delete(db_institution)
    await db.commit()
    return db_institution
