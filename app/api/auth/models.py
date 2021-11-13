from typing import Optional

from app.api.helpers.common import BaseModel
from app.api.users.models import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "ssdvsdvssdvlksdvssdv6sd8vs8dvsdvnsdvs",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "chandan005"
            }
        }
        
class UserTokenResponse(BaseModel):
    user: UserResponse
    token: Token