
from typing import Optional
from datetime import datetime, timedelta

from jose import jwt

from app.api.auth.models import *
from app.api.helpers.config import settings
from app.api.auth.security import verify_password
from app.api.helpers import deps

async def authenticate(username: str,password: str) -> Optional[UserResponse]:
    user = await deps.get_user_by_username_or_404(username=username)
    if not user:
        return None
    verified_pwd = verify_password(plain_password=password, hashed_password=user["password"])
    if not verified_pwd:
        return None
    return user

async def create_access_token(sub: str) -> str:
    data = await _create_token(token_type="access_token", lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),sub=sub)
    return  data
    
async def _create_token(token_type: str, lifetime: timedelta,sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
