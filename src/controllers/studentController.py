from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
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
    # Verificar si el estudiante existe
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()  # None si no existe el estudiante

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Verificar si el código o la cédula ya están en uso por otro estudiante
    conflict_field = None
    if student_data.cedula or student_data.codigo:
        query = select(Student).filter(Student.id != student_id)  # Excluir el estudiante actual
        if student_data.cedula:
            query = query.filter(Student.cedula == student_data.cedula)
            conflict_field = "cédula"
        if student_data.codigo:
            query = query.filter(Student.codigo == student_data.codigo)
            conflict_field = "código"

        existing_student = await db.execute(query)
        existing_student = existing_student.scalars().first()

        if existing_student:
            raise HTTPException(
                status_code=400,
                detail=f"El {conflict_field} ya está en uso por otro estudiante."
            )

    # Actualizar los campos de manera dinámica
    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    try:
        await db.commit()
        await db.refresh(student)  # Refrescar los datos actualizados
        return student
    except IntegrityError as e:
        # Manejar errores inesperados de base de datos
        raise HTTPException(
            status_code=400,
            detail="Error al actualizar el estudiante. Verifica los datos."
        )

# Eliminar un student
async def delete_student(db: AsyncSession, student_id: UUID):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted successfully"}
