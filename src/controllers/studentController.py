from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.models.studentModel import Student
from src.schemas.studentSchema import StudentCreate, StudentUpdate
from fastapi import HTTPException
from uuid import UUID

# Crear un student
async def create_student(db: AsyncSession, student: StudentCreate):
    # Verificar si ya existe un student con el mismo código o cédula
    existing_student = await db.execute(select(Student).filter(
        (Student.codigo == student.codigo) | (Student.cedula == student.cedula)
    ))
    existing_student = existing_student.scalars().first()
    
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="El código o la cédula ya están en uso."
        )
    
    # Si no hay duplicados, proceder a crear el student
    db_student = Student(
        codigo=student.codigo,
        nombre=student.nombre,
        cedula=student.cedula,
        correo=student.correo,
        numero_telefonico=student.numero_telefonico,
        fecha_nacimiento=student.fecha_nacimiento,
        estudiante_graduado =student.estudiante_graduado ,
    )
    db.add(db_student)
    await db.commit()
    return db_student

# Obtener estudiantes
async def get_students(db: AsyncSession):
    result = await db.execute(select(Student))
    return result.scalars().all()

# Obtener un student por ID
async def get_student_by_id(db: AsyncSession, student_id: UUID):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalars().first()
    return student

# Actualizar un student
async def update_student(db: AsyncSession, student_id: UUID, student_data: StudentUpdate):
    # Verificar si el student existe
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()  # None si no existe el student

    if not student:
        raise HTTPException(status_code=404, detail="Student no encontrado")

    # Verificar si el código o la cédula ya están en uso por otro student
    filter_conditions = []
    if student_data.codigo:
        filter_conditions.append(Student.codigo == student_data.codigo)
    if student_data.cedula:
        filter_conditions.append(Student.cedula == student_data.cedula)

    if filter_conditions:
        existing_student = await db.execute(select(Student).filter(
            *filter_conditions).filter(Student.id != student_id))  # Excluir al student actual
        existing_student = existing_student.scalars().first()

        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="El código o la cédula ya están en uso por otro student."
            )

    # Si no hay duplicados, proceder con la actualización
    if student_data.codigo:
        student.codigo = student_data.codigo
    if student_data.nombre:
        student.nombre = student_data.nombre
    if student_data.cedula:
        student.cedula = student_data.cedula
    if student_data.correo:
        student.correo = student_data.correo
    if student_data.numero_telefonico:
        student.numero_telefonico = student_data.numero_telefonico
    if student_data.fecha_nacimiento:
        student.fecha_nacimiento = student_data.fecha_nacimiento
    if student_data.estudiante_graduado  is not None:
        student.estudiante_graduado  = student_data.estudiante_graduado 

    await db.commit()
    return student

# Eliminar un student
async def delete_student(db: AsyncSession, student_id: UUID):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted successfully"}
