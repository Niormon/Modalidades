from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.models.studentModel import Estudiante
from src.schemas.studentSchema import StudentCreate, StudentUpdate
from fastapi import HTTPException

# Crear un estudiante
async def create_student(db: AsyncSession, student: StudentCreate):
    # Verificar si ya existe un estudiante con el mismo código o cédula
    existing_student = await db.execute(select(Estudiante).filter(
        (Estudiante.codigo == student.codigo) | (Estudiante.cedula == student.cedula)
    ))
    existing_student = existing_student.scalars().first()
    
    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="El código o la cédula ya están en uso."
        )
    
    # Si no hay duplicados, proceder a crear el estudiante
    db_student = Estudiante(
        codigo=student.codigo,
        nombre=student.nombre,
        cedula=student.cedula,
        correo=student.correo,
        numero_telefonico=student.numero_telefonico,
        fecha_nacimiento=student.fecha_nacimiento,
        estudiante_graduado=student.estudiante_graduado,
    )
    db.add(db_student)
    await db.commit()
    return db_student

# Obtener todos los estudiantes
async def get_students(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Estudiante).offset(skip).limit(limit))
    students = result.scalars().all()
    return students

# Obtener un estudiante por ID
async def get_student_by_id(db: AsyncSession, student_id: int):
    result = await db.execute(select(Estudiante).filter(Estudiante.id == student_id))
    student = result.scalars().first()
    return student

# Actualizar un estudiante
async def update_student(db: AsyncSession, student_id: int, student_data: StudentUpdate):
    # Verificar si el estudiante existe
    result = await db.execute(select(Estudiante).filter(Estudiante.id == student_id))
    student = result.scalar_one_or_none()  # None si no existe el estudiante

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Verificar si el código o la cédula ya están en uso por otro estudiante
    filter_conditions = []
    if student_data.codigo:
        filter_conditions.append(Estudiante.codigo == student_data.codigo)
    if student_data.cedula:
        filter_conditions.append(Estudiante.cedula == student_data.cedula)

    if filter_conditions:
        existing_student = await db.execute(select(Estudiante).filter(
            *filter_conditions).filter(Estudiante.id != student_id))  # Excluir al estudiante actual
        existing_student = existing_student.scalars().first()

        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="El código o la cédula ya están en uso por otro estudiante."
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
    if student_data.estudiante_graduado is not None:
        student.estudiante_graduado = student_data.estudiante_graduado

    await db.commit()
    return student

# Eliminar un estudiante
async def delete_student(db: AsyncSession, student_id: int):
    result = await db.execute(select(Estudiante).filter(Estudiante.id == student_id))
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {"message": "Student deleted successfully"}
