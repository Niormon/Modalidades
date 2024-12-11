from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.usuarioModel import Usuario
from src.models.rolModel import Rol
from src.models.rolPermisoModel import RolPermiso
from src.models.permisoModel import Permiso
from src.database.database import get_db
from src.utils.settings import settings

security = HTTPBearer()

def permiso_requerido(nombre_permiso: str):
    async def decorator(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db),
    ):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=403, detail="Token inválido o usuario no identificado.")

            # Buscar al usuario por nombre de usuario
            result = await db.execute(select(Usuario).filter(Usuario.nombre_usuario == username))
            usuario = result.scalars().first()
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            # Obtener el rol asociado al usuario
            result = await db.execute(select(Rol).filter(Rol.id == usuario.id_rol))
            rol = result.scalars().first()
            if not rol:
                raise HTTPException(status_code=403, detail="Rol del usuario no encontrado.")

            # Verificar los permisos del rol
            result = await db.execute(
                select(Permiso)
                .join(RolPermiso, Permiso.id == RolPermiso.id_permiso)
                .filter(RolPermiso.id_rol == rol.id)
            )
            rol_permisos = result.scalars().all()

            # Comprobar si el permiso solicitado está en la lista de permisos
            permiso_nombres = [permiso.nombre_permiso for permiso in rol_permisos]
            if nombre_permiso not in permiso_nombres:
                raise HTTPException(status_code=403, detail=f"Permiso '{nombre_permiso}' requerido.")

        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return decorator
