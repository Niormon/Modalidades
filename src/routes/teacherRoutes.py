from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.schemas.teacherSchema import TeacherCreate, TeacherUpdate, TeacherResponse
from uuid import UUID
from src.controllers.teacherController import (
    get_teachers, get_teacher, create_teacher, update_teacher, delete_teacher
)

TEACHER_ROUTES = APIRouter()

@TEACHER_ROUTES.get("/teachers/", response_model=list[TeacherResponse])
async def list_teachers(db: AsyncSession = Depends(get_db)):
    return await get_teachers(db)

@TEACHER_ROUTES.get("/teachers/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_by_id(teacher_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_teacher(db, teacher_id)

@TEACHER_ROUTES.post("/teachers/", response_model=TeacherResponse)
async def create_teacher_endpoint(teacher: TeacherCreate, db: AsyncSession = Depends(get_db)):
    return await create_teacher(db, teacher)

@TEACHER_ROUTES.put("/teachers/{teacher_id}", response_model=TeacherResponse)
async def update_teacher_endpoint(teacher_id: UUID, teacher: TeacherUpdate, db: AsyncSession = Depends(get_db)):
    return await update_teacher(db, teacher_id, teacher)

@TEACHER_ROUTES.delete("/teachers/{teacher_id}")
async def delete_teacher_endpoint(teacher_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_teacher(db, teacher_id)
