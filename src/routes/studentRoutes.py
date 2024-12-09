from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.controllers.studentController import create_student, get_students, get_student_by_id, update_student, delete_student
from src.schemas.studentSchema import StudentCreate, StudentUpdate, StudentResponse
from src.database.database import get_db

STUDENT_ROUTES = APIRouter()

# Crear un student
@STUDENT_ROUTES.post("/students/", response_model=StudentResponse)
async def create(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    return await create_student(db=db, student=student)

# Obtener estudiantes
@STUDENT_ROUTES.get("/students/", response_model=list[StudentResponse])
async def list_students(db: AsyncSession = Depends(get_db)):
    return await get_students(db)

# Obtener un student por ID
@STUDENT_ROUTES.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(student_id: UUID, db: AsyncSession = Depends(get_db)):
    student = await get_student_by_id(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Actualizar un student
@STUDENT_ROUTES.put("/students/{student_id}", response_model=StudentResponse)
async def update_student_info(student_id: UUID, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_student(db=db, student_id=student_id, student_data=student_data)

# Eliminar un student
@STUDENT_ROUTES.delete("/students/{student_id}", response_model=dict)
async def delete_student_info(student_id: UUID, db: AsyncSession = Depends(get_db)):
    return await delete_student(db=db, student_id=student_id)
