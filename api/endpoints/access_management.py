from fastapi import APIRouter
from Services.access_management_service import ban_user, unban_user
from pydantic import EmailStr, BaseModel
from fastapi import Depends
from Services.access_management_service import verify_jwt_token
from fastapi import HTTPException
import error_constants
from db_models.models.admin import AdminModel
from settings import oauth2_scheme


router = APIRouter()


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
