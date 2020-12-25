from fastapi import APIRouter
from Services.access_management_service import ban_user, unban_user
from pydantic import EmailStr, BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
import settings
from fastapi import HTTPException
import error_constants
from db_models.models.admin import AdminModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login/")

router = APIRouter()


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        """LOG JWT ERROR HERE"""
        print(e)
        return HTTPException(
            status_code=error_constants.TOKEN_EXPIRED_INVALID["status_code"],
            detail=error_constants.TOKEN_EXPIRED_INVALID["detail"]
        )


class BanModel(BaseModel):
    email: EmailStr


@router.post("/ban/")
def ban(
        ban_obj: BanModel,
        token: str = Depends(oauth2_scheme)
):
    payload = verify_jwt_token(token)
    try:
        AdminModel.objects.get(user_name=payload["sub"])
        ban_user(ban_obj.email)
        return True
    except AdminModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.INVALID_USER_NAME["status_code"],
            detail=error_constants.INVALID_USER_NAME["detail"]
        )



@router.post("/un_ban/")
def ban(
        ban_obj: BanModel,
        token: str = Depends(oauth2_scheme)
):
    payload = verify_jwt_token(token)
    try:
        AdminModel.objects.get(user_name=payload["sub"])
        unban_user(ban_obj.email)
        return True
    except AdminModel.DoesNotExist:
        raise HTTPException(
            status_code=error_constants.INVALID_USER_NAME["status_code"],
            detail=error_constants.INVALID_USER_NAME["detail"]
        )

