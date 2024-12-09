from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.controllers.studentController import create_student, get_students, get_student_by_id, update_student, delete_student
from src.schemas.studentSchema import StudentCreate, StudentUpdate, StudentResponse
from src.database.database import get_db

STUDENT_ROUTES = APIRouter()

# Crear un student
@STUDENT_ROUTES.post("/students/", response_model=StudentResponse)
async def create(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    return await create_student(db=db, student=student)

# Obtener todos los students
@STUDENT_ROUTES.get("/students/", response_model=list[StudentResponse])
async def read_students(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_students(db=db, skip=skip, limit=limit)

# Obtener un student por ID
@STUDENT_ROUTES.get("/students/{student_id}", response_model=StudentResponse)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_by_id(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Actualizar un student
@STUDENT_ROUTES.put("/students/{student_id}", response_model=StudentResponse)
async def update_student_info(student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_student(db=db, student_id=student_id, student_data=student_data)

# Eliminar un student
@STUDENT_ROUTES.delete("/students/{student_id}", response_model=dict)
async def delete_student_info(student_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_student(db=db, student_id=student_id)
