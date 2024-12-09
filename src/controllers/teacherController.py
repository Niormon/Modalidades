from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from src.models.teacherModel import Teacher
from src.schemas.teacherSchema import TeacherCreate, TeacherUpdate
from uuid import UUID

async def get_teachers(db: AsyncSession):
    result = await db.execute(select(Teacher))
    return result.scalars().all()

async def get_teacher(db: AsyncSession, teacher_id: UUID):
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

async def create_teacher(db: AsyncSession, teacher: TeacherCreate):
    try:
        new_teacher = Teacher(
            cedula=teacher.cedula,
            nombre=teacher.nombre,
            correo=teacher.correo,
            numero_telefonico=teacher.numero_telefonico
        )
        db.add(new_teacher)
        await db.commit()
        await db.refresh(new_teacher)
        return new_teacher
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="A teacher with this cedula already exists")

async def update_teacher(db: AsyncSession, teacher_id: UUID, teacher: TeacherUpdate):
    db_teacher = await db.get(Teacher, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Validate if cedula already exists
    existing_teacher = await db.execute(
        select(Teacher).where(Teacher.cedula == teacher.cedula, Teacher.id != teacher_id)
    )
    if existing_teacher.scalar():
        raise HTTPException(status_code=400, detail="A teacher with this cedula already exists")

    for key, value in teacher.dict(exclude_unset=True).items():
        setattr(db_teacher, key, value)

    await db.commit()
    await db.refresh(db_teacher)
    return db_teacher

async def delete_teacher(db: AsyncSession, teacher_id: UUID):
    db_teacher = await db.get(Teacher, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    await db.delete(db_teacher)
    await db.commit()
    return {"message": "Teacher deleted successfully"}
