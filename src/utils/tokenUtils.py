from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from src.utils.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
BLACKLIST = set()

def verify_token(token: str = Security(oauth2_scheme)):
    if token in BLACKLIST:
        raise HTTPException(status_code=401, detail="Token revocado")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
