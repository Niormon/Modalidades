from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.models.trackingModeModel import TrackingMode
from uuid import UUID

from src.models.modalityModel import Modality
from src.models.studentModel import Student
from src.models.teacherModel import Teacher
from src.models.institutionModel import Institution

async def get_tracking_modes(db: AsyncSession):
    result = await db.execute(
        select(TrackingMode)
        .options(
            joinedload(TrackingMode.modality),
            joinedload(TrackingMode.student),
            joinedload(TrackingMode.teacher),
            joinedload(TrackingMode.institution)
        )
    )
    tracking_modes = result.scalars().all()

    # Convertimos las fechas a formato string
    for mode in tracking_modes:
        if mode.fecha_inicio:
            mode.fecha_inicio = mode.fecha_inicio.strftime('%Y-%m-%d')
        if mode.fecha_fin:
            mode.fecha_fin = mode.fecha_fin.strftime('%Y-%m-%d')

    return tracking_modes

async def get_tracking_mode(db: AsyncSession, tracking_mode_id: UUID):
    result = await db.execute(
        select(TrackingMode)
        .options(
            joinedload(TrackingMode.modality),
            joinedload(TrackingMode.student),
            joinedload(TrackingMode.teacher),
            joinedload(TrackingMode.institution)
        )
        .filter(TrackingMode.id == tracking_mode_id)
    )
    tracking_mode = result.scalar_one_or_none()
    if not tracking_mode:
        raise HTTPException(status_code=404, detail="Tracking mode not found")
    return tracking_mode

async def create_tracking_mode(db: AsyncSession, tracking_mode):
    try:
        new_tracking_mode = TrackingMode(**tracking_mode.dict())
        db.add(new_tracking_mode)
        await db.commit()
        await db.refresh(new_tracking_mode)
        return new_tracking_mode
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data entry")

async def update_tracking_mode(db: AsyncSession, tracking_mode_id: UUID, tracking_mode_data):
    # Validar que TrackingMode exista
    tracking_mode = await db.get(TrackingMode, tracking_mode_id)
    if not tracking_mode:
        raise HTTPException(status_code=404, detail="Tracking mode not found")

    # Validar que modality_id exista
    if tracking_mode_data.modalidad_id is not None:
        modality_exists = await db.execute(
            select(Modality).where(Modality.id == tracking_mode_data.modalidad_id)
        )
        if not modality_exists.scalar():
            raise HTTPException(status_code=400, detail="Invalid modalidad_id: Not found in Modality table")

    # Validar que estudiante_id exista
    if tracking_mode_data.estudiante_id is not None:
        student_exists = await db.execute(
            select(Student).where(Student.id == tracking_mode_data.estudiante_id)
        )
        if not student_exists.scalar():
            raise HTTPException(status_code=400, detail="Invalid estudiante_id: Not found in Student table")

    # Validar que profesor_id exista
    if tracking_mode_data.profesor_id is not None:
        teacher_exists = await db.execute(
            select(Teacher).where(Teacher.id == tracking_mode_data.profesor_id)
        )
        if not teacher_exists.scalar():
            raise HTTPException(status_code=400, detail="Invalid profesor_id: Not found in Teacher table")

    # Validar que institucion_id exista
    if tracking_mode_data.institucion_id is not None:
        institution_exists = await db.execute(
            select(Institution).where(Institution.id == tracking_mode_data.institucion_id)
        )
        if not institution_exists.scalar():
            raise HTTPException(status_code=400, detail="Invalid institucion_id: Not found in Institution table")

    # Actualizar los campos del TrackingMode
    for key, value in tracking_mode_data.dict(exclude_unset=True).items():
        setattr(tracking_mode, key, value)

    try:
        await db.commit()
        await db.refresh(tracking_mode)
        return tracking_mode
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update tracking mode")

async def delete_tracking_mode(db: AsyncSession, tracking_mode_id: UUID):
    db_tracking_mode = await db.get(TrackingMode, tracking_mode_id)
    if not db_tracking_mode:
        raise HTTPException(status_code=404, detail="Tracking mode not found")

    await db.delete(db_tracking_mode)
    await db.commit()
    return {"message": "Tracking mode deleted successfully"}
