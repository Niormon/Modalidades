from fastapi import Depends, HTTPException, Header, APIRouter
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.schemas.tokenSchema import LoginRequest, TokenResponse, LogoutResponse
from src.controllers.authController import login, logout
from src.utils.settings import settings
from src.utils.tokenUtils import verify_token
from src.utils.authPerm import permiso_requerido


AUTH_ROUTER = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@AUTH_ROUTER.post("/login/", response_model=TokenResponse)
async def login_route(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login(db, data.username, data.password)

@AUTH_ROUTER.post("/logout/")
async def logout_route(
    authorization: str = Header(...),  # Token en el encabezado Authorization
    db: AsyncSession = Depends(get_db)
):
    # Extraer el token del encabezado
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
        return await logout(db, token, username)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@AUTH_ROUTER.get("/verify-token/")
async def verify_token_endpoint(payload: dict = Depends(verify_token)):
    # Retornar el payload decodificado como confirmación
    return {"status": "valid", "payload": payload}

@AUTH_ROUTER.get("/permissions/{nombre_permiso}/", dependencies=[Depends(permiso_requerido)])
async def verificar_permiso(nombre_permiso: str):
    """
    Verifica si el usuario tiene un permiso específico.
    """
    return {"status": "success", "message": f"Tienes el permiso '{nombre_permiso}'"}