from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from db_models.models.admin import AdminModel
from db_models.mongo_setup import global_init
from error_constants import INVALID_USER_NAME, INCORRECT_PASSWORD
from fastapi import HTTPException
from passlib.context import CryptContext
import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


global_init()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        admin_model_obj = AdminModel.objects.get(user_name=form_data.username)
        password_hash = admin_model_obj.password_hash
        if not verify_password(plain_password=form_data.password, hashed_password=password_hash):
            raise HTTPException(
                status_code=INCORRECT_PASSWORD["status_code"],
                detail=INCORRECT_PASSWORD["detail"]
            )
        else:
            access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": admin_model_obj.user_name}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
    except AdminModel.DoesNotExist:
        raise HTTPException(
            status_code=INVALID_USER_NAME["status_code"],
            detail=INVALID_USER_NAME["detail"]
        )