from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
from db_models.models.admin import AdminModel
from db_models.mongo_setup import global_init


global_init()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminRequestModel(BaseModel):
    user_name: str
    password: str


router = APIRouter()


@router.post("/signup/")
def ban(adm_obj: AdminRequestModel):
    admin_obj = AdminModel(user_name=adm_obj.user_name, password_hash=pwd_context.hash(adm_obj.password))
    admin_obj.save()
    return True
