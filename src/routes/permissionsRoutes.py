from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.usuarioModel import Usuario
from src.models.rolModel import Rol
from src.models.rolPermisoModel import RolPermiso
from src.models.permisoModel import Permiso
from src.database.database import get_db
from src.utils.settings import settings
from jose import jwt, JWTError

security = HTTPBearer()
PERMISSIONS_ROUTER = APIRouter()

@PERMISSIONS_ROUTER.get("/permissions/{nombre_permiso}/", tags=["permissions"])
async def check_permission(
    nombre_permiso: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    try:
        # Decodificar el token para obtener el nombre de usuario
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=403, detail="Token inválido o usuario no identificado.")

        # Buscar al usuario por nombre de usuario
        query_user = select(Usuario).filter(Usuario.nombre_usuario == username)
        result_user = await db.execute(query_user)
        usuario = result_user.scalars().first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        # Obtener el rol del usuario
        query_rol = select(Rol).filter(Rol.id == usuario.id_rol)
        result_rol = await db.execute(query_rol)
        rol = result_rol.scalars().first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol del usuario no encontrado.")

        # Verificar si el permiso está asociado al rol del usuario
        query_permiso = (
            select(Permiso)
            .join(RolPermiso, Permiso.id == RolPermiso.id_permiso)
            .filter(RolPermiso.id_rol == rol.id, Permiso.nombre_permiso == nombre_permiso)
        )
        result_permiso = await db.execute(query_permiso)
        permiso = result_permiso.scalars().first()

        if not permiso:
            raise HTTPException(status_code=403, detail=f"El rol del usuario no tiene el permiso '{nombre_permiso}'.")

        return {"status": "success", "message": f"Tienes el permiso '{nombre_permiso}'"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
