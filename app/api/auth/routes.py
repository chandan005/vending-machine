from app.api.users.models import UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth.models import UserResponse
from app.api.auth.repository import authenticate, create_access_token
from app.api.helpers.deps import fix_id, get_current_user

auth_router = APIRouter()

@auth_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = fix_id(data=user)
    act = await create_access_token(sub=user["username"])
    return {"access_token": act, "token_type": "bearer"}


@auth_router.post("/me", dependencies=[Depends(get_current_user)], response_model=UserResponse)
async def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user